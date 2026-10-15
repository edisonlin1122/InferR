"""
File: config.py

Purpose: This files contains the configuration settings for the InferR project.
It usage is to load env values from .env and sets up the paths for the project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Loads variables from .env
load_dotenv()

# Sets InferR/ as the BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Settings (grabs from .env)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
DEFAULT_DPI = int(os.getenv("DEFAULT_DPI", "150"))
SYSTEM_PROMPT_FILE = os.getenv("SYSTEM_PROMPT_FILE", "reasoning_instructions.txt")
CONTEXT_LAYOUT_FILE = os.getenv("CONTEXT_LAYOUT_FILE", "context_layout.txt")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "16384"))

# Paths
DATA_DIR = BASE_DIR / "data"
PROBLEMS_RAW = DATA_DIR / "problems" / "raw"
PROBLEMS_PARSED = DATA_DIR / "problems" / "parsed"
INSTRUCTIONS_RAW = DATA_DIR / "instructions" / "raw"
INSTRUCTIONS_PARSED = DATA_DIR / "instructions" / "parsed"
PROMPTS_DIR = BASE_DIR / "prompts"
OUTPUT_DIR = BASE_DIR / "output"
