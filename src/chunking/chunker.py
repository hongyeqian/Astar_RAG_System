"""
This module is chunker for the project
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from langchain_text_splitters import RecursiveCharacterTextSplitter

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader.loader import Meeting
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP



@dataclass
class ChunkMetadata:
    meeting_id: str
    level: str
    chunk_id: str
    text: str
    #metadata: Dict[str, Any]
    metadata: {}



class HierarchicalChunker:
    """Hierarchical chunker for the project"""


    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        """
        Initialize the hierarchical chunker

        Args:
            chunk_size: int = CHUNK_SIZE
            chunk_overlap: int = CHUNK_OVERLAP
        
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "；", "，", " ", ""]
            )



    def chunk_all_levels(self, meetings: List[Meeting]) -> Dict[str, List[ChunkMetadata]]:
        """
        chunk all levels for all meetings
        
        Args:
            meetings: list of meetings
            
        Returns:
            dictionary containing all level chunking results
        """
        result = {
            'metadata': [],
            'summary': [],
            'meeting': [],
            'conversation': [],
            'chunk': []
        }
        
        for meeting in meetings:
            result['metadata'].extend(self.chunk_metadata_level(meeting))
            result['summary'].extend(self.chunk_summary_level(meeting))
            result['meeting'].extend(self.chunk_meeting_level(meeting))
            result['conversation'].extend(self.chunk_conversation_level(meeting))
            result['chunk'].extend(self.chunk_fine_grained_level(meeting))
        
        print(f"\nChunking statistics:")
        print(f"  Metadata level: {len(result['metadata'])} chunks")
        print(f"  Summary level: {len(result['summary'])} chunks")
        print(f"  Meeting level: {len(result['meeting'])} chunks")
        print(f"  Conversation level: {len(result['conversation'])} chunks")
        print(f"  Chunk level: {len(result['chunk'])} chunks")
        
        return result


    def chunk_metadata_level(self, meeting: Meeting) -> List[ChunkMetadata]:
        """
        Metadata level: convert structured metadata (JSON) to text format for embedding
        """
        # construct structured text from Meeting.metadata (JSON dict)
        metadata_text_parts = [
            f"Meeting ID: {meeting.meeting_id}",
            f"Title: {meeting.title}",
            f"Date and Time: {meeting.datetime}",
            f"Duration: {meeting.duration_sec} seconds",
            f"Language: {meeting.language}",
            f"Meeting Type: {meeting.meeting_type}",
        ]
        
        # add participants information (for entity filtering)
        if meeting.participants:
            participants_str = ", ".join([
                f"{p.get('name', '')} ({p.get('role', '')})" 
                if isinstance(p, dict) else str(p)
                for p in meeting.participants
            ])
            metadata_text_parts.append(f"Participants: {participants_str}")
        
        # add organizations information (for entity filtering)
        if meeting.organizations:
            orgs_str = ", ".join(meeting.organizations)
            metadata_text_parts.append(f"Organizations: {orgs_str}")
        
        # add topics information (for topic filtering)
        if meeting.topics:
            topics_str = ", ".join(meeting.topics)
            metadata_text_parts.append(f"Topics: {topics_str}")
        
        # add keywords information (for topic filtering)
        if meeting.keywords:
            keywords_str = ", ".join(meeting.keywords)
            metadata_text_parts.append(f"Keywords: {keywords_str}")
        
        # add brief summary (for semantic understanding)
        if meeting.summary_brief:
            metadata_text_parts.append(f"Brief Summary: {meeting.summary_brief}")
        
        metadata_text = "\n".join(metadata_text_parts)
        
        return [ChunkMetadata(
            meeting_id=meeting.meeting_id,
            level='metadata',
            chunk_id=f"{meeting.meeting_id}_metadata",
            text=metadata_text,  # this text will be embedded, for semantic search
            metadata={
                'meeting_id': meeting.meeting_id,
                'title': meeting.title,
                'datetime': str(meeting.datetime),
                'duration_sec': meeting.duration_sec,
                'language': meeting.language,
                'meeting_type': meeting.meeting_type,
                'participants': meeting.participants,
                'organizations': meeting.organizations,
                'topics': meeting.topics,
                'keywords': meeting.keywords,
                'summary_brief': meeting.summary_brief
            }
        )]



    def chunk_summary_level(self, meeting: Meeting) -> List[ChunkMetadata]:
        """
        Summary level: the coarsest granularity, the entire summary as a chunk
        """
        return [ChunkMetadata(
            meeting_id=meeting.meeting_id,
            level='summary',
            chunk_id=f"{meeting.meeting_id}_summary",
            text=meeting.summary_text,
            metadata={
                'title': meeting.title,
                'datetime': str(meeting.datetime),
                'topics': meeting.topics,
                'keywords': meeting.keywords,
                'organizations': meeting.organizations
            }
        )]


    def chunk_meeting_level(self, meeting: Meeting) -> List[ChunkMetadata]:
        """
        Meeting level: the medium granularity, split meeting_level_text by paragraphs
        """
        chunks = []
        
        # split by double newline
        paragraphs = meeting.meeting_level_text.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        for idx, paragraph in enumerate(paragraphs):
            chunks.append(ChunkMetadata(
                meeting_id=meeting.meeting_id,
                level='meeting',
                chunk_id=f"{meeting.meeting_id}_meeting_{idx}",
                text=paragraph,
                metadata={
                    'title': meeting.title,
                    'datetime': str(meeting.datetime),
                    'paragraph_index': idx,
                    'topics': meeting.topics,
                    'keywords': meeting.keywords
                }
            ))
        
        return chunks



    def chunk_conversation_level(self, meeting: Meeting) -> List[ChunkMetadata]:
        """
        Conversation level: split by conversation turns
        """
        chunks = []
        
        # split by newline
        lines = meeting.conversation_text.split('\n')
        current_speaker = None
        current_text = []
        turn_index = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # check if it's a new speaker (assume format is "speaker: content")
            if ':' in line or '：' in line:
                # save previous speaker
                if current_speaker and current_text:
                    chunks.append(ChunkMetadata(
                        meeting_id=meeting.meeting_id,
                        level='conversation',
                        chunk_id=f"{meeting.meeting_id}_conv_{turn_index}",
                        text='\n'.join(current_text),
                        metadata={
                            'title': meeting.title,
                            'datetime': str(meeting.datetime),
                            'speaker': current_speaker,
                            'turn_index': turn_index
                        }
                    ))
                    turn_index += 1
                    current_text = []
                
                # extract speaker
                separator = ':' if ':' in line else '：'
                parts = line.split(separator, 1)
                current_speaker = parts[0].strip()
                if len(parts) > 1:
                    current_text.append(parts[1].strip())
            else:
                current_text.append(line)
        
        # save last speaker
        if current_speaker and current_text:
            chunks.append(ChunkMetadata(
                meeting_id=meeting.meeting_id,
                level='conversation',
                chunk_id=f"{meeting.meeting_id}_conv_{turn_index}",
                text='\n'.join(current_text),
                metadata={
                    'title': meeting.title,
                    'datetime': str(meeting.datetime),
                    'speaker': current_speaker,
                    'turn_index': turn_index
                }
            ))
        
        return chunks



    def chunk_fine_grained_level(self, meeting: Meeting) -> List[ChunkMetadata]:
        """
        Chunk level: the finest granularity, use RecursiveCharacterTextSplitter
        split the entire conversation
        """
        chunks = []
        
        # use langchain's text splitter
        text_chunks = self.splitter.split_text(meeting.conversation_text)
        
        for idx, text in enumerate(text_chunks):
            chunks.append(ChunkMetadata(
                meeting_id=meeting.meeting_id,
                level='chunk',
                chunk_id=f"{meeting.meeting_id}_chunk_{idx}",
                text=text,
                # metadata={
                #     'title': meeting.title,
                #     'datetime': str(meeting.datetime),
                #     'chunk_index': idx,
                #     'total_chunks': len(text_chunks)
                # }
                metadata={}
            ))
        
        return chunks


    
