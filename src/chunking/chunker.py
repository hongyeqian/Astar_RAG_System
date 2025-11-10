"""
This module is chunker for the project
Supports both standard hierarchical chunking and topic-aware graph chunking
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
import re

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
        Summary Level        ← Meeting summaries (split by individual summaries)
          ↓ details_in
        Meeting Level        ← Structured meeting content (split by topics with smart splitting)
    
    Summary level splits by individual summary sections. Meeting level splits by topics,
    ensuring each topic stays intact when possible, with overlap when splitting is needed.
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
                         include_chunk_level: bool = False) -> Dict[str, List[ChunkMetadata]]:
        """
        Chunk all levels for all meetings
        
        Args:
            meetings: list of meetings
            include_chunk_level: whether to include fine-grained chunk level (default: False)
                                Legacy parameter for compatibility, not recommended for use
            
        Returns:
            dictionary containing all level chunking results
        """
        # Initialize result dictionary
        result = {
            'metadata': [],
            'summary': [],
            'meeting': [],
        }
        
        if include_chunk_level:
            result['chunk'] = []
        
        # Process each meeting
        for meeting in meetings:
            result['metadata'].extend(self.chunk_metadata_level(meeting))
            result['summary'].extend(self.chunk_summary_level(meeting))
            result['meeting'].extend(self.chunk_meeting_level(meeting))
            
            if include_chunk_level:
                result['chunk'].extend(self.chunk_fine_grained_level(meeting))
        
        # Print statistics
        self._print_statistics(result)
        
        return result
    
    
    def _print_statistics(self, result: Dict[str, List[ChunkMetadata]]):
        """Print chunking statistics"""
        print(f"\n{'='*80}")
        print("HIERARCHICAL CHUNKING STATISTICS")
        print(f"{'='*80}")
        
        print(f"  Metadata level     : {len(result['metadata'])} chunks")
        print(f"  Summary level      : {len(result['summary'])} chunks")
        print(f"  Meeting level      : {len(result['meeting'])} chunks")
        
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
        Summary level: split by individual summary sections using MarkdownHeaderTextSplitter,
        then split long summaries at bullet point boundaries with bullet-level overlap
        """
        chunks = []
        
        # Use MarkdownHeaderTextSplitter to split by "## Summary" headers
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("##", "Summary")])
        md_splits = markdown_splitter.split_text(meeting.summary_text)
        
        chunk_counter = 0
        
        for summary_idx, md_doc in enumerate(md_splits):
            summary_content = md_doc.page_content
            
            # Extract metadata from summary content
            duration = self._extract_duration_from_text(summary_content)
            participants = self._extract_participants_from_text(summary_content)
            
            # Split summary at bullet point boundaries with bullet-level overlap
            sub_chunks = self._split_with_bullet_overlap(summary_content, chunk_size=1200)
            
            for part_idx, sub_chunk in enumerate(sub_chunks):
                chunk_id = f"{meeting.meeting_id}_summary_{chunk_counter}"
                
                # Extract timestamps from sub_chunk text
                sub_timestamps = self._extract_timestamps_from_sub_chunk(sub_chunk)
                
                # Build header
                summary_num = summary_idx + 1
                if len(sub_chunks) > 1:
                    header = f"## Summary {summary_num} (Part {part_idx + 1}/{len(sub_chunks)})"
                else:
                    header = f"## Summary {summary_num}"
                
                full_text = f"{header}\n\n{sub_chunk}\n\n" \
                          f"Meeting: {meeting.title}\n" \
                          f"Date: {meeting.datetime}"
                
                chunks.append(ChunkMetadata(
                    meeting_id=meeting.meeting_id,
                    level='summary',
                    chunk_id=chunk_id,
                    text=full_text,
                    metadata={
                        'title': meeting.title,
                        'datetime': str(meeting.datetime),
                        'topics': meeting.topics,
                        'keywords': meeting.keywords,
                        'organizations': meeting.organizations,
                        'summary_index': summary_idx + 1,
                        'duration': duration,
                        'participants': participants,
                        'timestamps': sub_timestamps,
                        'is_split': len(sub_chunks) > 1,
                        'split_part': f"{part_idx + 1}/{len(sub_chunks)}" if len(sub_chunks) > 1 else None,
                        'total_parts': len(sub_chunks) if len(sub_chunks) > 1 else None
                    }
                ))
                chunk_counter += 1
        
        return chunks
    
    def _split_with_bullet_overlap(self, text: str, chunk_size: int) -> List[str]:
        """
        Split text at bullet point boundaries with bullet-level overlap.
        Each chunk (except the first) starts with the last bullet point from the previous chunk.
        """
        # Split text into segments (bullet points and non-bullet text)
        segments = []
        current_segment = []
        is_bullet = False
        
        for line in text.split('\n'):
            line_stripped = line.strip()
            if line_stripped.startswith('- '):
                # Save previous segment if exists
                if current_segment:
                    segments.append(('\n'.join(current_segment), is_bullet))
                # Start new bullet segment
                current_segment = [line]
                is_bullet = True
            else:
                # Continue current segment
                if current_segment:
                    current_segment.append(line)
                else:
                    # Start new non-bullet segment
                    current_segment = [line]
                    is_bullet = False
        
        # Save last segment
        if current_segment:
            segments.append(('\n'.join(current_segment), is_bullet))
        
        # If no segments found, return original text
        if not segments:
            return [text] if text.strip() else []
        
        # If no bullet points found, return original text as single chunk
        if not any(is_bullet for _, is_bullet in segments):
            return [text] if text.strip() else []
        
        # Group segments into chunks with bullet-level overlap
        chunks = []
        current_chunk = []
        current_size = 0
        last_bullet_segment = None
        
        for segment, is_bullet_seg in segments:
            segment_size = len(segment)
            
            # If adding this segment would exceed chunk_size, start a new chunk
            if current_size + segment_size > chunk_size and current_chunk:
                # Save current chunk
                chunks.append('\n'.join(current_chunk))
                
                # Start new chunk with last bullet from previous chunk (overlap)
                if last_bullet_segment:
                    current_chunk = [last_bullet_segment, segment]
                    current_size = len(last_bullet_segment) + segment_size
                else:
                    current_chunk = [segment]
                    current_size = segment_size
            else:
                # Add to current chunk
                current_chunk.append(segment)
                current_size += segment_size
            
            # Update last bullet segment for overlap
            if is_bullet_seg:
                last_bullet_segment = segment
        
        # Add final chunk
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks if chunks else [text]
    
    def _extract_duration_from_text(self, text: str) -> str:
        """Extract duration from text"""
        for line in text.split('\n'):
            if '**Duration:**' in line or 'Duration:' in line:
                duration_match = re.search(r'\[([^\]]+)\]', line)
                if duration_match:
                    return duration_match.group(1)
        return ''
    
    def _extract_participants_from_text(self, text: str) -> str:
        """Extract participants from text"""
        for line in text.split('\n'):
            if '**Participants:**' in line or 'Participants:' in line:
                if ':' in line:
                    return line.split(':', 1)[1].strip()
        return ''

    def chunk_meeting_level(self, meeting: Meeting) -> List[ChunkMetadata]:
        """
        Meeting level: split by Key Topics and Action Items, then split individual topics
        
        Strategy:
        1. Use MarkdownHeaderTextSplitter to split Key Topics and Action Items
        2. Parse Key Topics section into individual topics (support both "- **Topic:**" and "- **Topic**" formats)
        3. For each topic: keep intact if short, or apply bullet-level overlap if long
        4. Extract and preserve timestamps from each topic
        """
        chunks = []
        
        # Use MarkdownHeaderTextSplitter to split Key Topics and Action Items
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[("##", "Key Topics"), ("##", "Action Items")]
        )
        md_splits = markdown_splitter.split_text(meeting.meeting_level_text)
        
        chunk_counter = 0
        
        for md_doc in md_splits:
            section_content = md_doc.page_content
            section_headers = md_doc.metadata
            
            # Check if this is Key Topics section
            # MarkdownHeaderTextSplitter stores headers in metadata with header text as key
            # e.g., {'Key Topics': 'Key Topics'} or {'Key Topics': 'Action Items'}
            section_title = section_headers.get('Key Topics', '')
            if section_title == 'Key Topics':
                # Parse Key Topics into individual topics
                topics = self._parse_key_topics(section_content)
                
                for topic_idx, topic_data in enumerate(topics):
                    topic_title = topic_data['title']
                    topic_content = topic_data['content']
                    duration = topic_data.get('duration', '')
                    participants = topic_data.get('participants', '')
                    
                    # Split topic at bullet point boundaries with bullet-level overlap if needed
                    sub_chunks = self._split_with_bullet_overlap(topic_content, chunk_size=1200)
                    
                    for part_idx, sub_chunk in enumerate(sub_chunks):
                        chunk_id = f"{meeting.meeting_id}_meeting_{chunk_counter}"
                        
                        # Extract timestamps from sub_chunk text
                        sub_timestamps = self._extract_timestamps_from_sub_chunk(sub_chunk)
                        
                        # Build header
                        if len(sub_chunks) > 1:
                            header = f"# {topic_title} (Part {part_idx + 1}/{len(sub_chunks)})"
                        else:
                            header = f"# {topic_title}"
                        
                        full_text = f"{header}\n\n{sub_chunk}\n\n" \
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
                                'topic_title': topic_title,
                                'topic_index': topic_idx,
                                'duration': duration,
                                'participants': participants,
                                'timestamps': sub_timestamps,
                                'is_split': len(sub_chunks) > 1,
                                'split_part': f"{part_idx + 1}/{len(sub_chunks)}" if len(sub_chunks) > 1 else None,
                                'total_parts': len(sub_chunks) if len(sub_chunks) > 1 else None
                            }
                        ))
                        chunk_counter += 1
            
            # Action Items section can be processed similarly if needed
            # For now, we skip Action Items as per the original implementation
        
        return chunks


    def _parse_key_topics(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse Key Topics section into individual topics
        
        Supports both formats:
        - "- **Topic Title:** ..." (with colon)
        - "- **Topic Title** ..." (without colon)
        
        Returns: List of dicts with 'title', 'content', 'duration', 'participants', 'timestamps'
        """
        topics = []
        lines = text.split('\n')
        
        current_topic = None
        current_content = []
        
        for i, line in enumerate(lines):
            # Match topic title: "- **Topic Title:**" or "- **Topic Title**"
            # Support both formats: with and without colon
            stripped = line.strip()
            if stripped.startswith('- **') and '**' in stripped:
                # Save previous topic
                if current_topic:
                    topic_dict = self._build_topic_dict(current_topic, '\n'.join(current_content))
                    if topic_dict:
                        topics.append(topic_dict)
                
                # Extract topic title - handle both formats
                topic_line = stripped
                if topic_line.startswith('- **'):
                    topic_line = topic_line[4:]  # Remove "- **"
                
                # Remove closing "**" and optional colon
                if ':**' in topic_line:
                    # Format: "- **Topic Title:** Description" or "- **Topic Title:**"
                    # Extract the part after ":**" as the actual topic title
                    parts = topic_line.split(':**', 1)
                    if len(parts) > 1 and parts[1].strip():
                        # If there's content after ":**", use it as topic title
                        current_topic = parts[1].strip()
                    else:
                        # Otherwise, use the part before ":**"
                        current_topic = parts[0].strip()
                elif topic_line.endswith('**'):
                    # Format: "- **Topic Title**"
                    current_topic = topic_line[:-2].strip()
                elif '**' in topic_line:
                    # Format: "- **Topic Title** rest of line"
                    parts = topic_line.split('**', 1)
                    current_topic = parts[0].strip()
                else:
                    current_topic = topic_line.strip()
                
                current_content = [line]
            elif stripped == '------':
                # Topic separator, save current topic
                if current_topic:
                    topic_dict = self._build_topic_dict(current_topic, '\n'.join(current_content))
                    if topic_dict:
                        topics.append(topic_dict)
                current_topic = None
                current_content = []
            else:
                # Accumulate content for current topic
                if current_topic is not None:
                    current_content.append(line)
        
        # Save last topic
        if current_topic:
            topic_dict = self._build_topic_dict(current_topic, '\n'.join(current_content))
            if topic_dict:
                topics.append(topic_dict)
        
        return topics
    
    def _build_topic_dict(self, topic_title: str, content: str) -> Dict[str, Any]:
        """Build topic dictionary with extracted metadata"""
        if not content.strip():
            return None
        
        # Extract duration
        duration = ''
        for line in content.split('\n'):
            if 'Duration:' in line or 'duration:' in line.lower():
                # Extract duration range like [00:12:15–00:18:40]
                duration_match = re.search(r'\[([^\]]+)\]', line)
                if duration_match:
                    duration = duration_match.group(1)
                break
        
        # Extract participants
        participants = ''
        for line in content.split('\n'):
            if 'Participants:' in line or 'participants:' in line.lower():
                participants = line.split(':', 1)[1].strip() if ':' in line else ''
                break
        
        # Extract all timestamps
        timestamps = self._extract_timestamps_from_text(content)
        
        return {
            'title': topic_title,
            'content': content.strip(),
            'duration': duration,
            'participants': participants,
            'timestamps': timestamps
        }
    
    def _extract_timestamps_from_sub_chunk(self, sub_chunk: str) -> List[str]:
        """
        Extract all timestamps from sub_chunk text.
        
        Uses the same logic as debug_timestamps.py:
        - Pattern: [HH:MM:SS] or [MM:SS]
        - Returns all timestamps found in the text
        """
        # Pattern for timestamps like [HH:MM:SS] or [MM:SS]
        # Same as debug_timestamps.py: r'\[(\d{2}:\d{2}(?::\d{2})?)\]'
        timestamp_pattern = r'\[(\d{2}:\d{2}(?::\d{2})?)\]'
        timestamps = re.findall(timestamp_pattern, sub_chunk)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_timestamps = []
        for ts in timestamps:
            if ts not in seen:
                seen.add(ts)
                unique_timestamps.append(ts)
        
        return unique_timestamps

    def _extract_timestamps_from_text(self, text: str) -> List[str]:
        """
        Extract all timestamps from text
        
        Expected formats:
        - [HH:MM:SS] ...
        - [00:12:15–00:18:40]
        - [HH:MM:SS–HH:MM:SS]
        """
        timestamps = []
        
        # Pattern for timestamps like [HH:MM:SS] or [00:12:15–00:18:40]
        timestamp_pattern = r'\[(\d{2}:\d{2}:\d{2}(?:–\d{2}:\d{2}:\d{2})?)\]'
        matches = re.findall(timestamp_pattern, text)
        
        for match in matches:
            if '–' in match:
                # Duration range, split into start and end
                start, end = match.split('–')
                timestamps.append(start.strip())
                timestamps.append(end.strip())
            else:
                timestamps.append(match.strip())
        
        # Also check for shorter format like [00:44] or [00:12:15–00:18:40]
        short_pattern = r'\[(\d{1,2}:\d{2}(?:–\d{1,2}:\d{2})?)\]'
        short_matches = re.findall(short_pattern, text)
        for match in short_matches:
            if match not in [t.split(':')[-1] if ':' in t else t for t in timestamps]:
                if '–' in match:
                    start, end = match.split('–')
                    timestamps.append(start.strip())
                    timestamps.append(end.strip())
                else:
                    timestamps.append(match.strip())
        
        # Remove duplicates while preserving order
        seen = set()
        unique_timestamps = []
        for ts in timestamps:
            if ts not in seen:
                seen.add(ts)
                unique_timestamps.append(ts)
        
        return unique_timestamps


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
