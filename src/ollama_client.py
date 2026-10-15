"""
File: ollama_client.py

Purpose: Communicates with the Ollama API to send prompts and images, and retrieves the model's response.
"""

import json
import re
import ollama
from src.config import OLLAMA_MODEL, MAX_TOKENS

def query_model(prompt: str, images: list[str] = None) -> dict:
    # Builds msg array with the user prompt
    messages = [{
        "role": "user", 
        "content": prompt
    }]

    # Injects img if it exists
    if images:
        messages[0]["images"] = images

    # Sets up Ollama API call with the model, messages, and constraints
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        format="json", 
        options={
            "num_ctx": MAX_TOKENS
        }
    )
    
    raw_content = response["message"]["content"].strip()

    # Extract structural JSON fields from markdown code block wrappers
    if raw_content.startswith("```"):
        match = re.search(r"```(?:json)?\s*([\s\(\S\)]*?)\s*```", raw_content)
        if match:
            raw_content = match.group(1).strip()
            
    return json.loads(raw_content)
