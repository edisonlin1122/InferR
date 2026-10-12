import fitz  # PyMuPDF
from pathlib import Path
from src.config import (
    PROBLEMS_RAW,
    PROBLEMS_PARSED,
    INSTRUCTIONS_RAW,
    INSTRUCTIONS_PARSED,
    DEFAULT_DPI,
)

SUPPORTED_EXTENSIONS = {
    "text": {".txt", ".md"},
    "pdf": {".pdf"},
    "image": {".png", ".jpg", ".jpeg", ".webp"}
}

def init_directories():

    directories = [
        PROBLEMS_RAW,
        PROBLEMS_PARSED,
        INSTRUCTIONS_RAW,
        INSTRUCTIONS_PARSED,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_file_type(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    for file_type, extensions in SUPPORTED_EXTENSIONS.items():
        if ext in extensions:
            return file_type


def _parse_text(file_path: Path) -> dict:
    return {"type": "text", "content": file_path.read_text(encoding="utf-8").strip()}


def _parse_image(file_path: Path) -> dict:
    return {"type": "image", "content": str(file_path)}


def _parse_pdf(file_path: Path, output_dir: Path, dpi: int) -> dict:
    target_folder = output_dir / file_path.stem
    target_folder.mkdir(parents=True, exist_ok=True)

    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    rendered_pages = []

    with fitz.open(file_path) as doc:
        for page_num, page in enumerate(doc):
            pix = page.get_pixmap(matrix=mat)
            output_file = target_folder / f"page_{page_num + 1}.png"
            pix.save(output_file)
            rendered_pages.append(str(output_file))

    return {"type": "pdf_images", "content": rendered_pages}


def parse_file(file_path: Path, output_dir: Path, dpi: int = DEFAULT_DPI) -> dict:

    init_directories()
    
    file_path = Path(file_path)
    file_type = get_file_type(file_path)

    if file_type == "text":
        return _parse_text(file_path)
    elif file_type == "image":
        return _parse_image(file_path)
    elif file_type == "pdf":
        return _parse_pdf(file_path, output_dir, dpi)
        
    raise ValueError(f"Unsupported file type: {file_type}")