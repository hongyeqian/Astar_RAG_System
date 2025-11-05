# this is a light demo for our project
import os, json, glob, re
from typing import List, Dict, Any, Optional, TypedDict
from datetime import datetime

# langgraph
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# some config we needed
EMBEDDING_DIM =1536

#print(os.getenv("OPENAI_API_KEY"))


#define the state
class RAGState(TypedDict):
    question: str
    filters: Dict[str, Any]
    meeting_docs: List[Document]
    chunk_docs: List[Document]
    answer: str


# data load and indexes
def load_meetings(path: str = "data/m*.json") -> List[Dict[str, Any]]:
    meetings = []
    for fp in glob.glob(path):
        with open(fp, encoding="utf-8") as f:
            meetings.append(json.load(f))

    return meetings


MEETINGS = load_meetings("data/m*.json")

# generate docs for meetings
def build_meeting_docs(meetings: List[Dict[str, Any]]) -> List[Document]:
    docs = []
    for m in meetings:
        meta ={
            "meeting_id": m["meeting_id"],
            "date": m["date"],
            "participants": ", ".join(m.get("participants", [])),
            "topic": m.get("topic", "")
        }
        
        # Build text from conversation or use summary
        if "conversation" in m:
            text = m.get("summary", "") + "\n" + "\n".join([f"{c['speaker']}: {c['text']}" for c in m["conversation"]])
        else:
            text = m.get("summary", "")
        
        docs.append(Document(page_content=text, metadata=meta))
    return docs


def build_chunk_documents(meetings: List[Dict[str, Any]]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    docs = []

    for m in meetings:
        meta ={
            "meeting_id": m["meeting_id"],
            "date": m["date"],
            "participants": ", ".join(m.get("participants", [])),
            "topic": m.get("topic", "")
        }
        
        # Build text from conversation or use summary
        if "conversation" in m:
            text = m.get("summary", "") + "\n" + "\n".join([f"{c['speaker']}: {c['text']}" for c in m["conversation"]])
        else:
            text = m.get("summary", "")

        splits = splitter.split_text(text)
        for i, chunk in enumerate(splits):
            md = dict(meta); md["chunk_id"] = f"{m['meeting_id']}#{i}"
            docs.append(Document(page_content=chunk, metadata=md))
    return docs


meeting_docs_all = build_meeting_docs(MEETINGS)
chunk_docs_all = build_chunk_documents(MEETINGS)


emb = OpenAIEmbeddings()
meeting_vs =FAISS.from_documents(meeting_docs_all, emb)
chunk_vs =FAISS.from_documents(chunk_docs_all, emb)


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)




# node

def parse_filters_node(state: RAGState) -> RAGState:
    q = state["question"]
    filters = {}
    m = re.search(r"(\d{4}-\d{2}-\d{2})", q)
    if m:
        filters["date_from"] = m.group(1)
    for name in ["Alice", "Bob", "Carol"]:
        if name.lower() in q.lower():
            filters["person"] = name
    if "RAG" in q or "rag" in q.lower():
        filters["topic"] = "RAG"
    state["filters"] = filters
    return state



def meeting_level_retrieval_node(state: RAGState) -> RAGState:
    q = state["question"]
    # simple method: filter metadata first, then do meeting vector retrieval
    k = 3
    docs = meeting_vs.similarity_search(q, k=k)
    # append post-processing based on filters
    f = state.get("filters", {})
    def ok(d: Document):
        md = d.metadata
        if f.get("person") and f["person"] not in md.get("participants",""):
            return False
        if f.get("topic") and f["topic"].lower() not in md.get("topic","").lower():
            return False
        if f.get("date_from") and md.get("date") < f["date_from"]:
            return False
        return True
    state["meeting_docs"] = [d for d in docs if ok(d)]
    return state



def chunk_level_retrieval_node(state: RAGState) -> RAGState:
    q = state["question"]
    # only search chunks in the meetings that are hit
    candidate_meeting_ids = {d.metadata["meeting_id"] for d in state.get("meeting_docs", [])}
    if not candidate_meeting_ids:
        # fallback: full search
        state["chunk_docs"] = chunk_vs.similarity_search(q, k=5)
        return state

    # filter chunk candidates
    docs = chunk_vs.similarity_search(q, k=20)
    hits = [d for d in docs if d.metadata.get("meeting_id") in candidate_meeting_ids]
    state["chunk_docs"] = hits[:5]
    return state


def answer_node(state: RAGState) -> RAGState:
    chunks = state.get("chunk_docs", [])
    if not chunks:
        state["answer"] = "Sorry, I couldn't find relevant content in the dummy data."
        return state

    # assemble reference context
    ctx = "\n\n".join(
        [f"[{i+1}] ({d.metadata['meeting_id']} | {d.metadata.get('date')})\n{d.page_content[:500]}"
         for i, d in enumerate(chunks)]
    )
    prompt = f"""You are a helpful assistant. Use the context to answer the question.
Question: {state['question']}


Context with citations:
{ctx}

Answer with 2-3 sentences and include citation numbers like [1],[2] when you use a piece of text.
"""
    resp = llm.invoke(prompt)
    state["answer"] = resp.content
    return state

# build LangGraph
graph = StateGraph(RAGState)
graph.add_node("parse_filters", parse_filters_node)
graph.add_node("meeting_retrieval", meeting_level_retrieval_node)
graph.add_node("chunk_retrieval", chunk_level_retrieval_node)
graph.add_node("answer", answer_node)

graph.set_entry_point("parse_filters")
graph.add_edge("parse_filters", "meeting_retrieval")
graph.add_edge("meeting_retrieval", "chunk_retrieval")
graph.add_edge("chunk_retrieval", "answer")
graph.add_edge("answer", END)

app = graph.compile()

if __name__ == "__main__":
    init_state: RAGState = {
        "question": "Who mentioned next steps for RAG in 2025-10-01? (maybe Alice?)",
        "filters": {},
        "meeting_docs": [],
        "chunk_docs": [],
        "answer": ""
    }
    out = app.invoke(init_state)
    print("\n=== ANSWER ===")
    print(out["answer"])
