"""
Test script for exporting hierarchical chunks to text files
This script exports all chunking results to organized text files for inspection
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader.loader import DataLoader
from src.chunking.chunker import HierarchicalChunker
from config.settings import DATA_DIR


def export_chunks_to_files(all_chunks, output_dir: Path):
    """
    Export all chunks to organized text files
    
    Args:
        all_chunks: Dictionary containing chunks at all levels
        output_dir: Output directory path
    """
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Export each level to a separate file (only if exists)
    available_levels = [level for level in ['metadata', 'summary', 'meeting', 'chunk'] 
                       if level in all_chunks and all_chunks[level]]
    
    for level in available_levels:
        chunks = all_chunks[level]
        output_file = output_dir / f"{level}_level_chunks.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write("="*100 + "\n")
            f.write(f"HIERARCHICAL CHUNKING RESULTS - {level.upper()} LEVEL\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Chunks: {len(chunks)}\n")
            f.write("="*100 + "\n\n")
            
            # Group chunks by meeting_id
            current_meeting = None
            
            for idx, chunk in enumerate(chunks):
                # Add separator between different meetings
                if chunk.meeting_id != current_meeting:
                    if current_meeting is not None:
                        f.write("\n" + "━"*100 + "\n")
                        f.write("━"*100 + "\n\n")
                    current_meeting = chunk.meeting_id
                    f.write(f">>> MEETING: {chunk.meeting_id} <<<\n")
                    f.write("━"*100 + "\n\n")
                
                # Write chunk information
                f.write(f"[CHUNK #{idx + 1}]\n")
                f.write(f"Chunk ID: {chunk.chunk_id}\n")
                f.write(f"Meeting ID: {chunk.meeting_id}\n")
                f.write(f"Level: {chunk.level}\n")
                
                # Write meeting-level specific metadata when available
                metadata = getattr(chunk, 'metadata', {}) or {}
                if chunk.level == 'meeting':
                    topic_id = metadata.get('topic_id')
                    reference = metadata.get('reference')
                    if topic_id:
                        f.write(f"Topic ID: {topic_id}\n")
                    if reference:
                        f.write(f"Reference: {reference}\n")
                    paragraph_refs = metadata.get('paragraph_indices')
                    if paragraph_refs:
                        f.write(f"Paragraph Indices: {', '.join(paragraph_refs)}\n")
                    duration = metadata.get('duration')
                    if duration:
                        f.write(f"Duration: {duration}\n")
                    participants = metadata.get('participants')
                    if participants:
                        f.write(f"Participants: {participants}\n")
                f.write(f"Text Length: {len(chunk.text)} characters\n")
                # f.write(f"\nMetadata:\n")
                # for key, value in chunk.metadata.items():
                #     f.write(f"  - {key}: {value}\n")
                f.write(f"\nText Content:\n")
                f.write("-"*100 + "\n")
                f.write(chunk.text)
                f.write("\n" + "-"*100 + "\n\n\n")
        
        print(f"[OK] Exported {len(chunks)} chunks to: {output_file}")


def generate_summary_report(all_chunks, output_dir: Path):
    """
    Generate a summary report of chunking statistics
    """
    report_file = output_dir / "chunking_summary_report.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write("HIERARCHICAL CHUNKING SUMMARY REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*100 + "\n\n")
        
        # Overall statistics
        f.write("OVERALL STATISTICS\n")
        f.write("-"*100 + "\n")
        total_chunks = sum(len(chunks) for chunks in all_chunks.values())
        f.write(f"Total Chunks (All Levels): {total_chunks}\n\n")
        
        # Per-level statistics
        f.write("PER-LEVEL STATISTICS\n")
        f.write("-"*100 + "\n")
        for level in ['metadata', 'summary', 'meeting', 'chunk']:
            if level in all_chunks:
                count = len(all_chunks[level])
                percentage = (count / total_chunks * 100) if total_chunks > 0 else 0
                f.write(f"{level.upper():15s}: {count:5d} chunks ({percentage:5.2f}%)\n")
            else:
                f.write(f"{level.upper():15s}: [DISABLED]\n")
        
        f.write("\n\n")
        
        # Per-meeting statistics
        f.write("PER-MEETING STATISTICS\n")
        f.write("-"*100 + "\n")
        
        meeting_stats = {}
        for level, chunks in all_chunks.items():
            for chunk in chunks:
                meeting_id = chunk.meeting_id
                # Skip global topic nodes
                if meeting_id == "GLOBAL":
                    continue
                if meeting_id not in meeting_stats:
                    meeting_stats[meeting_id] = {
                        'metadata': 0, 'summary': 0, 'meeting': 0,
                        'chunk': 0, 'total': 0
                    }
                if level in meeting_stats[meeting_id]:
                    meeting_stats[meeting_id][level] += 1
                    meeting_stats[meeting_id]['total'] += 1
        
        for meeting_id in sorted(meeting_stats.keys()):
            stats = meeting_stats[meeting_id]
            f.write(f"\n{meeting_id}:\n")
            f.write(f"  Metadata     : {stats['metadata']:4d} chunks\n")
            f.write(f"  Summary      : {stats['summary']:4d} chunks\n")
            f.write(f"  Meeting      : {stats['meeting']:4d} chunks\n")
            f.write(f"  Chunk        : {stats['chunk']:4d} chunks\n")
            f.write(f"  Total        : {stats['total']:4d} chunks\n")
        
        f.write("\n\n")
        
        # Text length statistics
        f.write("TEXT LENGTH STATISTICS\n")
        f.write("-"*100 + "\n")
        for level in ['metadata', 'summary', 'meeting', 'chunk']:
            if level not in all_chunks:
                continue
            chunks = all_chunks[level]
            if chunks:
                lengths = [len(chunk.text) for chunk in chunks]
                avg_length = sum(lengths) / len(lengths)
                min_length = min(lengths)
                max_length = max(lengths)
                f.write(f"\n{level.upper()} Level:\n")
                f.write(f"  Average Length: {avg_length:8.2f} characters\n")
                f.write(f"  Min Length    : {min_length:8d} characters\n")
                f.write(f"  Max Length    : {max_length:8d} characters\n")
        
        f.write("\n" + "="*100 + "\n")
    
    print(f"[OK] Summary report generated: {report_file}")


def main():
    """Main execution function"""
    print("="*100)
    print("HIERARCHICAL CHUNKING TEST - Export to Files")
    print("="*100)
    
    # Step 1: Load data
    print("\n[Step 1] Loading meeting data...")
    loader = DataLoader(DATA_DIR)
    meetings = loader.load_all_meetings()
    
    # Step 2: Perform chunking
    print("\n[Step 2] Performing hierarchical chunking...")
    chunker = HierarchicalChunker()
    
    # Chunk all levels (metadata, summary, meeting)
    all_chunks = chunker.chunk_all_levels(
        meetings, 
        include_chunk_level=False
    )
    
    # Step 3: Export to files
    print("\n[Step 3] Exporting chunks to text files...")
    output_dir = project_root / "output" / "chunking_results"
    export_chunks_to_files(all_chunks, output_dir)
    
    # Step 4: Generate summary report
    print("\n[Step 4] Generating summary report...")
    generate_summary_report(all_chunks, output_dir)
    
    # Final message
    print("\n" + "="*100)
    print("EXPORT COMPLETED SUCCESSFULLY!")
    print("="*100)
    print(f"\nOutput directory: {output_dir.absolute()}")
    print("\nGenerated files:")
    file_num = 1
    for level in ['metadata', 'summary', 'meeting', 'chunk']:
        if level in all_chunks and all_chunks[level]:
            print(f"  {file_num}. {level}_level_chunks.txt")
            file_num += 1
    print(f"  {file_num}. chunking_summary_report.txt")


if __name__ == "__main__":
    main()
