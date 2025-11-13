# README.md



## Project Overview

This is a Retrieval-Augmented Generation (RAG) system implementing hierarchical chunking for meeting transcripts. The system processes meeting data through multiple granularity levels (metadata, summary, meeting topics, conversations) to enable effective semantic search and retrieval.

## Core Architecture

### Data Flow
```
Raw Meeting Data (datademo/con*/)
  └─> DataLoader (src/data_loader/loader.py)
      └─> Meeting objects (with metadata, summary, transcript)
          └─> HierarchicalChunker (src/chunking/chunker.py)
              └─> ChunkMetadata objects (3 levels by default)
                  └─> EmbeddingGenerator (src/embeddings/generator.py)
                      └─> Vector embeddings for retrieval
```

### Hierarchical Chunking Levels

The system implements a 3-level hierarchy for retrieval:

1. **Metadata Level**: Meeting metadata converted to searchable text (participants, topics, keywords, brief summary)
   - One chunk per meeting, not split

2. **Summary Level**: High-level meeting summaries treated as single documents
   - Entire summary text split using bullet-level overlap at 1200 characters
   - Extracts `summary_ids` (S001-T01, S001-A01) and `references` (M001-T01) for mapping to meeting level

3. **Meeting Level**: Detailed topic/action item content split by semantic boundaries
   - Split by individual topics/action items (- **Topic Title:** or - **Responsible Person:**)
   - Only applies bullet-level overlap if a single topic/item exceeds 1200 characters
   - Extracts `entry_id` (M001-T01, M001-A01) and `reference` (P001-P002) for mapping to paragraphs

A legacy "chunk level" exists but is disabled by default (`include_chunk_level=False`) as it splits text without semantic boundaries.

### Key Components

**DataLoader** (`src/data_loader/loader.py`):
- Loads meeting data from `datademo/con*/` directories
- Each meeting has: `metaData*.json`, `data*.md` (transcript), `meetLevel*.json` or `.md` (topic summaries), `summary*.md` (embedding summaries)
- Supports both JSON and text/markdown formats for meeting-level data
- Automatically adds paragraph indices `[#P001]` to transcript files for reference tracking

**HierarchicalChunker** (`src/chunking/chunker.py`):
- Core chunking logic with 3 main methods: `chunk_metadata_level()`, `chunk_summary_level()`, `chunk_meeting_level()`
- Uses `MarkdownHeaderTextSplitter` from LangChain to split by section headers
- Smart splitting strategy: bullet-level overlap preserves semantic context
- Extracts IDs and references to establish clear retrieval hierarchy mapping

**EmbeddingGenerator** (`src/embeddings/generator.py`):
- Wraps OpenAI embeddings with batch processing and optional caching
- Supports single query embeddings and batch document embeddings
- Default model: `text-embedding-3-small` (1536 dimensions)

### Configuration

Settings are in `config/settings.py`:
- `DATA_DIR`: Path to meeting data (default: `datademo/`)
- `CHUNK_SIZE`: 800 characters (for legacy chunk level only)
- `CHUNK_OVERLAP`: 120 characters (for legacy chunk level only)
- `EMBEDDING_MODEL`: `text-embedding-3-small`
- API keys loaded from `.env` file (not committed)

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Tests
```bash
# Export all chunking results to text files
python tests/test_chunking_export.py

# Output will be in: output/chunking_results/
# Files generated:
#   - metadata_level_chunks.txt
#   - summary_level_chunks.txt
#   - meeting_level_chunks.txt
#   - chunking_summary_report.txt

# Debug timestamp extraction
python tests/debug_timestamps.py

# Debug paragraph indices extraction
python tests/test_meeting_level_paragraph_indices.py
```

### Running Individual Modules
```bash
# Test data loader
python src/data_loader/loader.py

# Test chunker
python src/chunking/chunker.py

# Test embedding generator (requires OpenAI API key)
python src/embeddings/generator.py
```

## Data Format Specifications

### Meeting Data Structure

Each meeting is stored in a `datademo/con*/` directory with these files:

**metaData*.json**: Meeting metadata including:
- `meeting_id`, `title`, `datetime`, `duration_sec`
- `participants`: list of `{name, role}` objects
- `organizations`, `topics`, `keywords`
- `summary_brief`: one-sentence summary
- `related_files`: pointers to other files

**data*.md**: Raw transcript with conversation turns
- Format: `[#P001] [HH:MM:SS] Speaker: Content`
- Paragraph indices `[#P001]` are auto-added by DataLoader

**meetLevel*.md**: Topic-level detailed summaries
- Markdown format with `## Key Topics` and `## Action Items` sections
- Each entry starts with `- **Topic Title:**` or `- **Responsible Person:**`
- Contains: Topic id (M001-T01), Reference (P001-P002), Summary bullets, Participants, Duration
- Entries may be separated by `------` dividers (optional)

**summary*.md**: High-level meeting summaries for quick retrieval
- Markdown format with meeting header: `## M001 — Title`
- Each entry format: `- **[S001-T01] Topic: ...` or `- **[S001-A01] Action: ...`
- Contains: summary_id, description, Reference to meeting-level (e.g., M001-T01)
- Establishes Summary → Meeting retrieval hierarchy

### Important Parsing Logic

**Summary ID Format**: `S001-T01` (Summary 001, Topic 01) or `S001-A01` (Summary 001, Action 01)

**Meeting ID Format**: `M001-T01` (Meeting 001, Topic 01) or `M001-A01` (Meeting 001, Action 01)

**Reference Parsing**:
- Paragraph range: `P001–P002` expands to `[#P001, #P002]`
- Discrete paragraphs: `P004,P008` expands to `[#P004, #P008]`
- Meeting references: `M001-T01, M001-T04` (can have multiple references)

**Timestamp Pattern**: `\[(\d{2}:\d{2}(?::\d{2})?)\]` matches `[HH:MM:SS]` or `[MM:SS]`

**Paragraph Index Pattern**: `\[#P(\d+)\]` matches `[#P001]`, `[#P002]`, etc.

## Important Implementation Details

### Chunking Strategy

1. **Metadata Level**: One chunk per meeting
   - All metadata converted to searchable text
   - Not split

2. **Summary Level**: Treat entire summary as single document
   - Split using bullet-level overlap at 1200 characters
   - Extract all `summary_ids` and `references` from each chunk
   - Chunk may contain multiple summary entries

3. **Meeting Level**: Split by semantic boundaries (topics/action items)
   - First split by `## Key Topics` and `## Action Items` sections
   - Then split by individual entries (`- **Topic Title:**` or `- **Responsible Person:**`)
   - Only apply bullet-level overlap if single entry > 1200 characters
   - Keep complete topics/items together when possible

### 3-Level Retrieval Hierarchy

Clear mapping relationships for retrieval navigation:

```
Summary Level (High-level abstractions)
  ↓ references
Meeting Level (Detailed topic/action content)
  ↓ references
Data Level (Raw transcript paragraphs)
```

**Example Mapping**:
- Summary: `S001-T01` → references → `M001-T01`
- Meeting: `M001-T01` → references → `P001-P002` → expands to `[#P001, #P002]`

### Metadata Extraction

ChunkMetadata objects store:
- `meeting_id`, `level`, `chunk_id`, `text` (for embedding)
- `metadata` dict with level-specific info:
  - **Summary level**: `summary_ids` (list), `references` (list of M###-T##/A##)
  - **Meeting level**: `section`, `entry_id` (M###-T##/A##), `reference` (P###-P###), `paragraph_indices` (list)

### Smart Splitting with Overlap

The `_split_with_bullet_overlap()` method:
1. Parses text into segments (bullet vs non-bullet)
2. Groups segments into chunks ≤ chunk_size
3. When splitting, starts new chunk with last bullet from previous chunk (provides context)
4. This preserves semantic coherence better than character-based splitting

## Code Patterns

### Loading and Chunking
```python
from src.data_loader.loader import DataLoader
from src.chunking.chunker import HierarchicalChunker
from config.settings import DATA_DIR

loader = DataLoader(DATA_DIR)
meetings = loader.load_all_meetings()

chunker = HierarchicalChunker()
all_chunks = chunker.chunk_all_levels(
    meetings,
    include_chunk_level=False  # Disable legacy chunk level
)

# Access chunks by level
metadata_chunks = all_chunks['metadata']
summary_chunks = all_chunks['summary']
meeting_chunks = all_chunks['meeting']
```

### Generating Embeddings
```python
from src.embeddings.generator import EmbeddingGenerator

generator = EmbeddingGenerator()

# Single query embedding
query_embedding = generator.generate_embedding("your query")

# Batch embeddings by level
embeddings_by_level = generator.generate_embeddings_by_level(
    all_chunks,
    batch_size=100,
    use_cache=False
)
```

## Development Notes

- The system uses OpenAI API for embeddings - ensure `.env` has `OPENAI_API_KEY`
- The `Astar_RAG_System/` directory appears to be a duplicate/backup - main code is in `src/`
- The `rubbishBin/` directory contains old data - use `datademo/` for active data
- Virtual environment is in `.venv/` (not committed)
- Output files go to `output/` directory (not committed)

## Future Development Areas

Based on code comments and structure:
- Retrieval system not yet implemented (settings exist: `TOP_K_SUMMARY`, `TOP_K_MEETING`, `TOP_K_CHUNK`)
- Vector store integration (FAISS is installed but not used yet)
- Multi-level retrieval with hierarchy navigation (Summary → Meeting → Data)
- Graph-based retrieval using reference relationships
