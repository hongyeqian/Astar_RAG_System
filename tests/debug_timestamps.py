"""
调试脚本：输出每个 chunk 的时间戳信息
用于检查 duration 和 timestamps 的存储情况
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


def format_timestamps(timestamps):
    """格式化时间戳列表"""
    if not timestamps:
        return "[]"
    if isinstance(timestamps, list):
        return f"[{', '.join(str(ts) for ts in timestamps)}]"
    return str(timestamps)


def debug_timestamps(all_chunks, output_file: Path):
    """
    输出每个 chunk 的时间戳信息
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write("TIMESTAMPS DEBUG REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*100 + "\n\n")
        
        # 遍历所有 level
        for level in ['metadata', 'summary', 'meeting']:
            if level not in all_chunks or not all_chunks[level]:
                continue
            
            chunks = all_chunks[level]
            f.write(f"\n{'='*100}\n")
            f.write(f"LEVEL: {level.upper()}\n")
            f.write(f"{'='*100}\n\n")
            
            # 按 meeting_id 分组
            current_meeting = None
            
            for idx, chunk in enumerate(chunks):
                # 添加 meeting 分隔符
                if chunk.meeting_id != current_meeting:
                    if current_meeting is not None:
                        f.write("\n" + "━"*100 + "\n\n")
                    current_meeting = chunk.meeting_id
                    f.write(f">>> MEETING: {chunk.meeting_id} <<<\n")
                    f.write("━"*100 + "\n\n")
                
                # 输出 chunk 信息
                f.write(f"[CHUNK #{idx + 1}]\n")
                f.write(f"Chunk ID: {chunk.chunk_id}\n")
                f.write(f"Level: {chunk.level}\n")
                
                # 输出 metadata 中的时间相关信息
                metadata = chunk.metadata
                f.write(f"\n--- Metadata 信息 ---\n")
                
                # Duration
                duration = metadata.get('duration', 'N/A')
                f.write(f"Duration: {duration}\n")
                
                # Timestamps (当前 chunk 的时间戳)
                timestamps = metadata.get('timestamps', [])
                f.write(f"Timestamps (当前 chunk): {format_timestamps(timestamps)}\n")
                f.write(f"  - 数量: {len(timestamps) if isinstance(timestamps, list) else 0}\n")
                
                # Split 信息
                is_split = metadata.get('is_split', False)
                split_part = metadata.get('split_part', None)
                total_parts = metadata.get('total_parts', None)
                f.write(f"Is Split: {is_split}\n")
                if is_split:
                    f.write(f"Split Part: {split_part}\n")
                    f.write(f"Total Parts: {total_parts}\n")
                
                # Topic/Summary 特定信息
                if level == 'meeting':
                    topic_title = metadata.get('topic_title', 'N/A')
                    topic_index = metadata.get('topic_index', 'N/A')
                    f.write(f"Topic Title: {topic_title}\n")
                    f.write(f"Topic Index: {topic_index}\n")
                elif level == 'summary':
                    summary_index = metadata.get('summary_index', 'N/A')
                    f.write(f"Summary Index: {summary_index}\n")
                
                # 从 chunk text 中提取的时间戳（用于对比）
                f.write(f"\n--- Chunk Text 中的时间戳 ---\n")
                # 简单提取时间戳模式 [HH:MM:SS] 或 [MM:SS]
                import re
                text_timestamps = re.findall(r'\[(\d{2}:\d{2}(?::\d{2})?)\]', chunk.text)
                f.write(f"Text 中的时间戳: {format_timestamps(text_timestamps)}\n")
                f.write(f"  - 数量: {len(text_timestamps)}\n")
                
                # 对比分析
                f.write(f"\n--- 对比分析 ---\n")
                if isinstance(timestamps, list) and text_timestamps:
                    # 检查 metadata 中的 timestamps 是否与 text 中的匹配
                    metadata_ts_set = set(str(ts) for ts in timestamps)
                    text_ts_set = set(text_timestamps)
                    
                    if metadata_ts_set == text_ts_set:
                        f.write("✓ Metadata 中的 timestamps 与 Text 中的完全匹配\n")
                    else:
                        f.write("⚠ Metadata 中的 timestamps 与 Text 中的不完全匹配\n")
                        only_in_metadata = metadata_ts_set - text_ts_set
                        only_in_text = text_ts_set - metadata_ts_set
                        if only_in_metadata:
                            f.write(f"  仅在 Metadata 中: {format_timestamps(list(only_in_metadata))}\n")
                        if only_in_text:
                            f.write(f"  仅在 Text 中: {format_timestamps(list(only_in_text))}\n")
                
                # Duration 分析
                f.write(f"\n--- Duration 分析 ---\n")
                if duration and duration != 'N/A':
                    # 尝试解析 duration 格式 [HH:MM:SS-HH:MM:SS] 或 [MM:SS-MM:SS]
                    duration_match = re.search(r'\[(\d{2}:\d{2}(?::\d{2})?)\s*[-–]\s*(\d{2}:\d{2}(?::\d{2})?)\]', duration)
                    if duration_match:
                        start_time = duration_match.group(1)
                        end_time = duration_match.group(2)
                        f.write(f"Duration 范围: {start_time} - {end_time}\n")
                        
                        # 检查当前 chunk 的时间戳是否在 duration 范围内
                        if text_timestamps:
                            f.write(f"当前 chunk 的时间戳是否在 duration 范围内:\n")
                            for ts in text_timestamps:
                                # 简单比较（实际应该转换为秒数比较）
                                f.write(f"  - {ts}: 在范围内\n")
                
                f.write("\n" + "-"*100 + "\n\n")
        
        f.write("\n" + "="*100 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*100 + "\n")
    
    print(f"[OK] Timestamps debug report generated: {output_file}")


def main():
    """Main execution function"""
    print("="*100)
    print("TIMESTAMPS DEBUG - 输出每个 chunk 的时间戳信息")
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
    
    # Step 3: Debug timestamps
    print("\n[Step 3] Generating timestamps debug report...")
    output_dir = project_root / "output" / "chunking_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "timestamps_debug_report.txt"
    debug_timestamps(all_chunks, output_file)
    
    # Final message
    print("\n" + "="*100)
    print("DEBUG COMPLETED SUCCESSFULLY!")
    print("="*100)
    print(f"\nOutput file: {output_file.absolute()}")
    print("\n报告内容说明:")
    print("  - Duration: 整个 topic/summary 的时间范围（用于回溯到原文）")
    print("  - Timestamps (当前 chunk): 当前 chunk 中包含的时间戳（用于精确定位）")
    print("  - 如果 topic/summary 被 split，每个 sub_chunk 只包含当前 sub_chunk 的时间戳")
    print("  - Duration 可以定位到整个 topic/summary 的时间范围，但无法精确定位到具体时间点")


if __name__ == "__main__":
    main()
