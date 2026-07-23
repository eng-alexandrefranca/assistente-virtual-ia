import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DATA_DIR = os.getenv("DATA_DIR", "data")
DOCS_DIR = os.getenv("DOCS_DIR", "docs")
VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "vectorstore")
