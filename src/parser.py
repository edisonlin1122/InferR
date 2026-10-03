import os
from pypdf import PdfReader

SUPPORTED_FORMATS = {
    'text': {'.txt', '.md'},
    'pdf': {'.pdf'},
    'image': {'.png', '.jpg', '.jpeg', '.webp'}
}

def get_file_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    for file_type, extensions in SUPPORTED_FORMATS.items():
        if ext in extensions:
            return file_type
    raise ValueError(f"Unsupported format: {ext}")

def parse_file(file_path: str) -> dict:
    file_type = get_file_type(file_path)
    
    if file_type == "text":
        with open(file_path, 'r', encoding='utf-8') as f:
            return {"type": "text", "content": f.read().strip()}
            
    if file_type == "pdf":
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return {"type": "text", "content": text.strip()}
        
    if file_type == "image":
        return {"type": "image", "content": file_path}