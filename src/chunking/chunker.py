"""
This module is chunker for the project
Supports both standard hierarchical chunking and topic-aware graph chunking
"""

from typing import List, Dict, Any, Set, Tuple
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
    """
    Hierarchical chunker for meeting transcripts
    
    Architecture:
        Metadata Level       ← Meeting metadata (with topic filter)
          ↓ summarizes
        Summary Level        ← Meeting summaries
          ↓ details_in
        Meeting Level        ← Structured meeting content (semantic sections with smart splitting)
          ↓ contains
        Topic Level (opt)    ← LLM-generated topic summaries (per meeting)
    
    The topic level provides intermediate granularity for focused retrieval on 
    specific topics discussed within a meeting. Meeting level uses intelligent
    splitting that balances semantic coherence with chunk size constraints.
    """


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



    def chunk_all_levels(self, 
                         meetings: List[Meeting], 
                         include_chunk_level: bool = False,
                         include_topic_level: bool = True) -> Dict[str, List[ChunkMetadata]]:
        """
        Chunk all levels for all meetings
        
        Args:
            meetings: list of meetings
            include_chunk_level: whether to include fine-grained chunk level (default: False)
                                Legacy parameter for compatibility, not recommended for use
            include_topic_level: whether to include topic level chunks (default: True)
                                Provides intermediate granularity between meeting and summary levels
            
        Returns:
            dictionary containing all level chunking results
        """
        # Initialize result dictionary
        result = {
            'metadata': [],
            'summary': [],
            'meeting': [],
        }
        
        if include_topic_level:
            result['topic'] = []
        
        if include_chunk_level:
            result['chunk'] = []
        
        # Process each meeting
        for meeting in meetings:
            result['metadata'].extend(self.chunk_metadata_level(meeting))
            result['summary'].extend(self.chunk_summary_level(meeting))
            result['meeting'].extend(self.chunk_meeting_level(meeting))
            
            if include_topic_level:
                result['topic'].extend(self.chunk_topic_level(meeting))
            
            if include_chunk_level:
                result['chunk'].extend(self.chunk_fine_grained_level(meeting))
        
        # Print statistics
        self._print_statistics(result, include_topic_level)
        
        return result
    
    
    def _print_statistics(self, result: Dict[str, List[ChunkMetadata]], include_topic_level: bool):
        """Print chunking statistics"""
        print(f"\n{'='*80}")
        print("HIERARCHICAL CHUNKING STATISTICS")
        print(f"{'='*80}")
        
        print(f"  Metadata level     : {len(result['metadata'])} chunks")
        print(f"  Summary level      : {len(result['summary'])} chunks")
        print(f"  Meeting level      : {len(result['meeting'])} chunks")
        
        if include_topic_level and 'topic' in result:
            print(f"  Topic level        : {len(result['topic'])} chunks")
        elif 'topic' not in result:
            print(f"  Topic level        : [DISABLED] (use include_topic_level=True to enable)")
        
        if 'chunk' in result:
            if result['chunk']:
                print(f"  Chunk level        : {len(result['chunk'])} chunks [Legacy - Not Recommended]")
            else:
                print(f"  Chunk level        : [DISABLED]")
        else:
            print(f"  Chunk level        : [DISABLED] (use include_chunk_level=True to enable)")
        
        print(f"{'='*80}\n")


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
        Meeting level: semantic sections with intelligent splitting
        
        Strategy:
        1. Parse by H2/H3 headers to maintain semantic boundaries
        2. For sections < 1200 chars: keep intact
        3. For sections ≥ 1200 chars: apply overlapping split
        
        This balances semantic coherence with retrieval efficiency.
        """
        chunks = []
        sections = self._parse_meeting_markdown(meeting.meeting_level_text)
        
        # Initialize text splitter for long sections
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,      # Target size for long sections
            chunk_overlap=150,     # Overlap to preserve context
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunk_counter = 0
        
        for section_idx, (section_title, section_content) in enumerate(sections):
            # Check section length
            section_length = len(section_content)
            
            if section_length < 1200:
                # Keep short sections intact
                chunk_id = f"{meeting.meeting_id}_meeting_{chunk_counter}"
                
                full_text = f"# {section_title}\n\n{section_content}\n\n" \
                        f"Meeting: {meeting.title}\n" \
                        f"Date: {meeting.datetime}"
                
                chunks.append(ChunkMetadata(
                    meeting_id=meeting.meeting_id,
                    level='meeting',
                    chunk_id=chunk_id,
                    text=full_text,
                    metadata={
                        'title': meeting.title,
                        'datetime': str(meeting.datetime),
                        'topics': meeting.topics,
                        'keywords': meeting.keywords,
                        'section_title': section_title,
                        'section_index': section_idx,
                        'is_split': False,
                        'split_part': None
                    }
                ))
                chunk_counter += 1
                
            else:
                # Split long sections with overlap
                sub_chunks = text_splitter.split_text(section_content)
                
                for part_idx, sub_chunk in enumerate(sub_chunks):
                    chunk_id = f"{meeting.meeting_id}_meeting_{chunk_counter}"
                    
                    # Add section context to each sub-chunk
                    full_text = f"# {section_title} (Part {part_idx + 1}/{len(sub_chunks)})\n\n" \
                            f"{sub_chunk}\n\n" \
                            f"Meeting: {meeting.title}\n" \
                            f"Date: {meeting.datetime}"
                    
                    chunks.append(ChunkMetadata(
                        meeting_id=meeting.meeting_id,
                        level='meeting',
                        chunk_id=chunk_id,
                        text=full_text,
                        metadata={
                            'title': meeting.title,
                            'datetime': str(meeting.datetime),
                            'topics': meeting.topics,
                            'keywords': meeting.keywords,
                            'section_title': section_title,
                            'section_index': section_idx,
                            'is_split': True,
                            'split_part': f"{part_idx + 1}/{len(sub_chunks)}",
                            'total_parts': len(sub_chunks)
                        }
                    ))
                    chunk_counter += 1
        
        return chunks


    def _parse_meeting_markdown(self, text: str) -> List[Tuple[str, str]]:
        """
        Parse meetLevel*.md into sections based on H2 (##) and H3 (###) headers
        
        Strategy:
        - H2 sections that are NOT "Key Topics" → single section
        - "Key Topics" section → split by H3, each topic becomes a separate section
        
        Returns: List of (section_title, section_content) tuples
        """
        sections = []
        lines = text.split('\n')
        current_h2_section = None
        current_h3_section = None
        current_content = []
        in_key_topics = False
        
        for line in lines:
            # Match H2 headers (## Title)
            if line.startswith('## '):
                # Save previous section before starting new H2
                if current_h2_section:
                    if in_key_topics and current_h3_section:
                        # Save the last H3 in Key Topics
                        sections.append((current_h3_section, '\n'.join(current_content).strip()))
                    elif not in_key_topics:
                        # Save the H2 section (not Key Topics)
                        sections.append((current_h2_section, '\n'.join(current_content).strip()))
                
                # Start new H2 section
                current_h2_section = line[3:].strip().replace('*', '')  # Remove markdown bold
                in_key_topics = ('Key Topics' in current_h2_section or 
                                'Key Topics' in line)
                current_h3_section = None
                current_content = []
                
            # Match H3 headers (### N. Topic Name)
            elif line.startswith('### '):
                if in_key_topics:
                    # Save previous H3 topic if exists
                    if current_h3_section and current_content:
                        sections.append((current_h3_section, '\n'.join(current_content).strip()))
                    
                    # Start new H3 topic
                    topic_name = line[4:].strip().replace('*', '')  # Remove markdown bold
                    current_h3_section = f"Key Topics — {topic_name}"
                    current_content = []
                else:
                    # H3 outside Key Topics, treat as content
                    current_content.append(line)
            
            else:
                current_content.append(line)
        
        # Save the last section
        if current_h2_section:
            if in_key_topics and current_h3_section:
                sections.append((current_h3_section, '\n'.join(current_content).strip()))
            elif not in_key_topics:
                sections.append((current_h2_section, '\n'.join(current_content).strip()))
        
        return sections


    def chunk_topic_level(self, meeting: Meeting) -> List[ChunkMetadata]:
        """
        Topic level: structured summaries of each topic discussed in the meeting
        
        This level provides intermediate granularity between summary and meeting levels.
        Each topic is presented as an LLM-generated structured summary with key points.
        
        Topic chunks belong to a specific meeting and enable focused retrieval on 
        specific topics within a meeting.
        """
        chunks = []
        
        # Parse the topic markdown file
        # Expected format: "## Topic Name" followed by bullet points
        topic_sections = self._parse_topic_markdown(meeting.topic_text)
        
        for topic_idx, (topic_name, topic_content) in enumerate(topic_sections):
            chunk_id = f"{meeting.meeting_id}_topic_{topic_idx}"
            
            # Construct full topic text with context
            full_text = f"# {topic_name}\n\n{topic_content}\n\n" \
                       f"Meeting: {meeting.title}\n" \
                       f"Date: {meeting.datetime}"
            
            chunks.append(ChunkMetadata(
                meeting_id=meeting.meeting_id,
                level='topic',
                chunk_id=chunk_id,
                text=full_text,
                metadata={
                    'topic_name': topic_name,
                    'parent_meeting': meeting.meeting_id,
                    'title': meeting.title,
                    'datetime': str(meeting.datetime),
                    'topic_index': topic_idx,
                    'all_topics': meeting.topics
                }
            ))
        
        return chunks
    
    
    def _parse_topic_markdown(self, topic_text: str) -> List[tuple]:
        """
        Parse topic markdown into sections
        
        Returns:
            List of (topic_name, topic_content) tuples
        """
        sections = []
        lines = topic_text.split('\n')
        
        current_topic = None
        current_content = []
        
        for line in lines:
            # Check if it's a topic header (## Topic Name)
            if line.strip().startswith('## '):
                # Save previous topic
                if current_topic is not None:
                    sections.append((current_topic, '\n'.join(current_content)))
                
                # Start new topic
                current_topic = line.strip()[3:].strip()  # Remove "## "
                current_content = []
            else:
                # Accumulate content for current topic
                if current_topic is not None and line.strip():
                    current_content.append(line)
        
        # Save last topic
        if current_topic is not None:
            sections.append((current_topic, '\n'.join(current_content)))
        
        return sections





    def chunk_fine_grained_level(self, meeting: Meeting) -> List[ChunkMetadata]:
        """
        [LEGACY - NOT RECOMMENDED]
        Chunk level: the finest granularity, use RecursiveCharacterTextSplitter
        to split raw conversation text without semantic boundaries.
        
        This is kept for compatibility but not recommended. Use meeting level 
        with smart splitting instead, which preserves semantic coherence.
        """
        chunks = []
        
        # use langchain's text splitter on raw conversation
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
