import os
from pathlib import Path
from dotenv import load_dotenv

# Loads variables from .env
load_dotenv()

# Sets InferR/ as the BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Settings
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
DEFAULT_DPI = int(os.getenv("DEFAULT_DPI", "150"))

# Paths
DATA_DIR = BASE_DIR / "data"
PROBLEMS_RAW = DATA_DIR / "problems" / "raw"
PROBLEMS_PARSED = DATA_DIR / "problems" / "parsed"
INSTRUCTIONS_RAW = DATA_DIR / "instructions" / "raw"
INSTRUCTIONS_PARSED = DATA_DIR / "instructions" / "parsed"