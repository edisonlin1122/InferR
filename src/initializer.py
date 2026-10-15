"""
File: initializer.py

Purpose: This file essentially sets up all the directories & paths, ensuring they exist.
"""

import shutil
from src.config import (
    PROBLEMS_RAW,
    PROBLEMS_PARSED,
    INSTRUCTIONS_RAW,
    INSTRUCTIONS_PARSED,
    PROMPTS_DIR,
    OUTPUT_DIR
)

def make_dirs():
    for parsed_dir in [PROBLEMS_PARSED, INSTRUCTIONS_PARSED]:
        if parsed_dir.exists():
            shutil.rmtree(parsed_dir)
            
    required_paths = [
        PROBLEMS_RAW,
        PROBLEMS_PARSED,
        INSTRUCTIONS_RAW,
        INSTRUCTIONS_PARSED,
        PROMPTS_DIR,
        OUTPUT_DIR
    ]
    for path in required_paths:
        path.mkdir(parents=True, exist_ok=True)

