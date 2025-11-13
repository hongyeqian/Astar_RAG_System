"""
Test script to verify paragraph indices in meeting level chunks
Validates that each chunk's paragraph_indices correctly match the paragraph indices in the chunk text
"""

import sys
from pathlib import Path
from datetime import datetime
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader.loader import DataLoader
from src.chunking.chunker import HierarchicalChunker
from config.settings import DATA_DIR


def extract_paragraph_indices_from_text(text: str) -> list[str]:
    """
    Extract all paragraph indices from text using multiple patterns:
    1. Direct markers: [#P001], [#P002], etc.
    2. Reference line: [Paragraph References: #P001, #P002, ...]
    """
    indices = []
    
    # Pattern 1: Direct markers like [#P001], [#P002]
    direct_pattern = r'\[#P(\d+)\]'
    direct_matches = re.findall(direct_pattern, text)
    for idx in direct_matches:
        formatted_idx = f"#P{idx.zfill(3)}"
        if formatted_idx not in indices:
            indices.append(formatted_idx)
    
    # Pattern 2: Reference line like [Paragraph References: #P001, #P002, ...]
    ref_pattern = r'\[Paragraph References:\s*([^\]]+)\]'
    ref_match = re.search(ref_pattern, text)
    if ref_match:
        ref_text = ref_match.group(1)
        # Extract #P001, #P002, etc. from the reference text
        ref_indices = re.findall(r'#P(\d+)', ref_text)
        for idx in ref_indices:
            formatted_idx = f"#P{idx.zfill(3)}"
            if formatted_idx not in indices:
                indices.append(formatted_idx)
    
    return indices


def test_meeting_level_paragraph_indices(all_chunks: dict, output_file: Path):
    """
    Test that each meeting level chunk's paragraph_indices correctly match the indices in chunk text
    """
    if 'meeting' not in all_chunks or not all_chunks['meeting']:
        print("No meeting level chunks found")
        return
    
    chunks = all_chunks['meeting']
    total_chunks = len(chunks)
    passed_tests = 0
    failed_tests = 0
    test_results = []
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write("MEETING LEVEL PARAGRAPH INDICES TEST REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total chunks to test: {total_chunks}\n")
        f.write("="*100 + "\n\n")
        
        # Group chunks by meeting_id
        current_meeting = None
        
        for idx, chunk in enumerate(chunks):
            # Add meeting separator
            if chunk.meeting_id != current_meeting:
                if current_meeting is not None:
                    f.write("\n" + "━"*100 + "\n\n")
                current_meeting = chunk.meeting_id
                f.write(f">>> MEETING: {chunk.meeting_id} <<<\n")
                f.write("━"*100 + "\n\n")
            
            # Extract paragraph indices from chunk text
            text_indices = extract_paragraph_indices_from_text(chunk.text)
            
            # Get paragraph indices from metadata
            metadata_indices = chunk.metadata.get('paragraph_indices', [])
            
            # Print to console for verification
            print(f"\n[CHUNK #{idx + 1}] {chunk.chunk_id}")
            print(f"  Topic: {chunk.metadata.get('topic_title', 'N/A')}")
            print(f"  Extracted from text: {text_indices}")
            print(f"  Metadata paragraph_indices: {metadata_indices}")
            
            # Convert to sets for comparison
            text_indices_set = set(text_indices)
            metadata_indices_set = set(metadata_indices)
            
            # Test: metadata indices should match text indices
            test_passed = text_indices_set == metadata_indices_set
            
            if not test_passed:
                only_in_text = text_indices_set - metadata_indices_set
                only_in_metadata = metadata_indices_set - text_indices_set
                if only_in_text:
                    print(f"  ⚠️  Only in text: {sorted(only_in_text)}")
                if only_in_metadata:
                    print(f"  ⚠️  Only in metadata: {sorted(only_in_metadata)}")
            else:
                print(f"  ✓ Match!")
            
            if test_passed:
                passed_tests += 1
            else:
                failed_tests += 1
            
            # Record test result
            result = {
                'chunk_id': chunk.chunk_id,
                'meeting_id': chunk.meeting_id,
                'topic_title': chunk.metadata.get('topic_title', 'N/A'),
                'topic_id': chunk.metadata.get('topic_id', 'N/A'),  # Use topic_id instead of topic_index
                'is_split': chunk.metadata.get('is_split', False),
                'split_part': chunk.metadata.get('split_part', None),
                'text_indices': text_indices,
                'metadata_indices': metadata_indices,
                'passed': test_passed
            }
            test_results.append(result)
            
            # Write test result
            f.write(f"[CHUNK #{idx + 1}]\n")
            f.write(f"Chunk ID: {chunk.chunk_id}\n")
            f.write(f"Topic Title: {result['topic_title']}\n")
            f.write(f"Topic ID: {result['topic_id']}\n")  # Use topic_id instead of topic_index
            f.write(f"Is Split: {result['is_split']}\n")
            if result['is_split']:
                f.write(f"Split Part: {result['split_part']}\n")
            
            f.write(f"\n--- Test Result ---\n")
            f.write(f"Status: {'✓ PASSED' if test_passed else '✗ FAILED'}\n")
            f.write(f"Paragraph indices in text: {text_indices}\n")
            f.write(f"  - Count: {len(text_indices)}\n")
            f.write(f"Paragraph indices in metadata: {metadata_indices}\n")
            f.write(f"  - Count: {len(metadata_indices)}\n")
            
            if not test_passed:
                f.write(f"\n--- Mismatch Details ---\n")
                only_in_text = text_indices_set - metadata_indices_set
                only_in_metadata = metadata_indices_set - text_indices_set
                
                if only_in_text:
                    f.write(f"Indices only in text: {sorted(only_in_text)}\n")
                if only_in_metadata:
                    f.write(f"Indices only in metadata: {sorted(only_in_metadata)}\n")
            
            f.write("\n" + "-"*100 + "\n\n")
        
        # Summary
        f.write("\n" + "="*100 + "\n")
        f.write("TEST SUMMARY\n")
        f.write("="*100 + "\n\n")
        f.write(f"Total chunks tested: {total_chunks}\n")
        f.write(f"Passed: {passed_tests}\n")
        f.write(f"Failed: {failed_tests}\n")
        f.write(f"Success rate: {(passed_tests/total_chunks*100):.2f}%\n")
        
        if failed_tests > 0:
            f.write(f"\n--- Failed Chunks ---\n")
            for result in test_results:
                if not result['passed']:
                    f.write(f"  - {result['chunk_id']} (Topic: {result['topic_title']})\n")
        
        f.write("\n" + "="*100 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*100 + "\n")
    
    # Print summary to console
    print(f"\n{'='*100}")
    print("TEST SUMMARY")
    print(f"{'='*100}")
    print(f"Total chunks tested: {total_chunks}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(passed_tests/total_chunks*100):.2f}%")
    
    if failed_tests > 0:
        print(f"\nFailed chunks:")
        for result in test_results:
            if not result['passed']:
                print(f"  - {result['chunk_id']} (Topic: {result['topic_title']})")
    
    return passed_tests, failed_tests, test_results


def main():
    """Main execution function"""
    print("="*100)
    print("MEETING LEVEL PARAGRAPH INDICES TEST")
    print("="*100)
    
    # Step 1: Load data
    print("\n[Step 1] Loading meeting data...")
    loader = DataLoader(DATA_DIR)
    meetings = loader.load_all_meetings()
    print(f"  Loaded {len(meetings)} meetings")
    
    # Step 2: Perform chunking
    print("\n[Step 2] Performing hierarchical chunking...")
    chunker = HierarchicalChunker()
    
    # Chunk all levels (metadata, summary, meeting)
    all_chunks = chunker.chunk_all_levels(
        meetings, 
        include_chunk_level=False
    )
    
    meeting_chunks = all_chunks.get('meeting', [])
    print(f"  Generated {len(meeting_chunks)} meeting level chunks")
    
    # Step 3: Test paragraph indices
    print("\n[Step 3] Testing paragraph indices...")
    output_dir = project_root / "output" / "chunking_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "meeting_level_paragraph_indices_test.txt"
    
    passed, failed, results = test_meeting_level_paragraph_indices(all_chunks, output_file)
    
    # Final message
    print("\n" + "="*100)
    if failed == 0:
        print("ALL TESTS PASSED!")
    else:
        print(f"TESTS COMPLETED: {passed} passed, {failed} failed")
    print("="*100)
    print(f"\nOutput file: {output_file.absolute()}")


if __name__ == "__main__":
    main()
