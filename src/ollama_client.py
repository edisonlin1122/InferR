import ollama
from src.config import OLLAMA_MODEL

def query_model(prompt: str, images: list[str] = None) -> dict:
    messages = [{
        "role": "user", 
        "content": prompt
        }]
    
    if images:
        messages[0]["images"] = images

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        format="json", 
    )
    
    import json
    return json.loads(response["message"]["content"])