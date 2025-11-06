"""
This module is data loader for the project
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Meeting:
    # from metaData.json
    meeting_id: str
    title: str
    datetime: datetime
    duration_sec: int
    language: str
    source_url: str
    meeting_type: str
    participants: List[Dict[str, Any]]
    organizations: List[str]
    topics: List[str]
    keywords: List[str]
    summary_brief: str

    # from data*.md
    conversation_text: str
    # from meetLevel*.md
    meeting_level_text: str
    # from summary*.md
    summary_text: str


    # from metaData.json
    metadata: Dict[str, Any]



class DataLoader:
    """Load data from datademo"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        
    def load_all_meetings(self) -> List[Meeting]:
        """Load all meetings data"""
        meetings = []
        
        # iterate all con* folders
        for con_dir in sorted(self.data_dir.glob("con*")):
            if not con_dir.is_dir():
                continue
                
            try:
                meeting = self._load_meeting(con_dir)
                meetings.append(meeting)
                print(f"Success Loaded: {meeting.meeting_id} - {meeting.title}")
            except Exception as e:
                print(f"Fail Error loading {con_dir.name}: {e}")
                
        print(f"\n Total meetings loaded: {len(meetings)}")
        return meetings
    
    def _load_meeting(self, con_dir: Path) -> Meeting:
        """Load single meeting data"""
        # 1. read metadata JSON
        metadata_file = self._find_file(con_dir, "metaData*.json")
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # 2. read text files
        conversation_file = self._find_file(con_dir, metadata['related_files']['transcript'])
        meeting_level_file = self._find_file(con_dir, metadata['related_files']['meeting_summary'])
        summary_file = self._find_file(con_dir, metadata['related_files']['summary_embedding'])
        
        conversation_text = self._read_text_file(conversation_file)
        meeting_level_text = self._read_text_file(meeting_level_file)
        summary_text = self._read_text_file(summary_file)
        
        # 3. construct Meeting object
        return Meeting(
            meeting_id=metadata['meeting_id'],
            title=metadata['title'],
            datetime=metadata['datetime'],
            duration_sec=metadata['duration_sec'],
            language=metadata['language'],
            source_url=metadata['source_url'],
            meeting_type=metadata['meeting_type'],
            participants=metadata['participants'],
            organizations=metadata['organizations'],
            topics=metadata['topics'],
            keywords=metadata['keywords'],
            summary_brief=metadata['summary_brief'],
            conversation_text=conversation_text,
            meeting_level_text=meeting_level_text,
            summary_text=summary_text,
            metadata=metadata
        )
    
    def _find_file(self, directory: Path, filename: str) -> Path:
        """find file (support wildcard and case-insensitive)"""
        # try direct match first
        direct_path = directory / filename
        if direct_path.exists():
            return direct_path
        
        # try wildcard match
        matches = list(directory.glob(filename))
        if matches:
            return matches[0]
        
        # try case-insensitive match
        for file in directory.iterdir():
            if file.name.lower() == filename.lower():
                return file
        
        raise FileNotFoundError(f"File not found: {filename} in {directory}")
    
    def _read_text_file(self, filepath: Path) -> str:
        """read text file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()


# testing code
if __name__ == "__main__":
    import sys
    from pathlib import Path
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))
    from config.settings import DATA_DIR
    
    loader = DataLoader(DATA_DIR)
    meetings = loader.load_all_meetings()
    
    # print first meeting information
    if meetings:
        m = meetings[7]
        print(f"1.  meeting_id: {m.meeting_id}")
        print(f"2.  title: {m.title}")
        print(f"3.  datetime: {m.datetime}")
        print(f"4.  duration_sec: {m.duration_sec}")
        print(f"5.  language: {m.language}")
        print(f"6.  source_url: {m.source_url}")
        print(f"7.  meeting_type: {m.meeting_type}")
        print(f"8.  participants: {m.participants}")
        print(f"9.  organizations: {m.organizations}")
        print(f"10. topics: {m.topics}")
        print(f"11. keywords: {m.keywords}")
        print(f"12. summary_brief: {m.summary_brief}")
        print(f"13. conversation_text: {m.conversation_text[:100]}...")
        print(f"14. meeting_level_text: {m.meeting_level_text[:100]}...")
        print(f"15. summary_text: {m.summary_text[:100]}...")
        print(f"16. metadata: {m.metadata}")
