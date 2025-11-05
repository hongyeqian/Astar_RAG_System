import os
from pathlib import Path
from dotenv import load_dotenv



load_dotenv()

# config path, may be need
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "datademo"
# write future path here

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#print(OPENAI_API_KEY)
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
#print(OPENAI_MODEL, EMBEDDING_MODEL)

# Chunking settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


# retrieval settings
TOP_K_SUMMARY = 3
TOP_K_MEETING = 3
TOP_K_CHUNK = 5


# following is the necessary settings for the project
# will write future
