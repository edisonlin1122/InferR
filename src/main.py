"""
File: main.py

Purpose:
The main file that sets up all the paths, and loads the prompts into the Ollama model.
It loads all of the assets (problems and instructions), compiles it into a payload for the model to handle.
It will output a JSON file with the model's response, as well as a PDF version for clear human-readability.
"""

import sys
import json
from pathlib import Path
from src.config import (
    PROBLEMS_RAW, PROBLEMS_PARSED, INSTRUCTIONS_RAW, INSTRUCTIONS_PARSED, PROMPTS_DIR, SYSTEM_PROMPT_FILE, CONTEXT_LAYOUT_FILE, OUTPUT_DIR
)

from src.parser import parse_file
from src.ollama_client import query_model
from src.pdf_generator import generate_pdf_report
from src.initializer import make_dirs

# This function loads the system prompt and just returns the content as string
def load_sys_prompt() -> str:
    prompt_path = PROMPTS_DIR / SYSTEM_PROMPT_FILE
    if not prompt_path.exists():
        raise FileNotFoundError(f"System prompt missing at: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")

# This function loads the context layout and just returns the content as string
def load_context_layout() -> str:
    layout_path = PROMPTS_DIR / CONTEXT_LAYOUT_FILE
    if not layout_path.exists():
        raise FileNotFoundError(f"Context layout missing at: {layout_path}")
    return layout_path.read_text(encoding="utf-8")


# Iterates through files inside a directory and combines them into an a big asset map
def process_folder(raw_dir: Path, parsed_dir: Path, global_images: list[str]) -> str:
    text_manifests = []

    # Sorts the fles
    for file_path in sorted(raw_dir.iterdir()):
        if file_path.is_dir() or file_path.name.startswith("."):
            continue

        try:
            target_folder = parsed_dir / file_path.stem
            # Reuse previously parsed PDF images if they exist, otherwise parse the file
            if file_path.suffix.lower() == ".pdf" and target_folder.exists() and any(target_folder.iterdir()):
                rendered_pages = [str(p) for p in sorted(target_folder.iterdir()) if p.suffix == ".png"]
                parsed_data = {"type": "pdf_images", "content": rendered_pages}
            else:
                parsed_data = parse_file(file_path, output_dir=parsed_dir)
            
            abs_path = str(file_path.resolve())
            
            # Format plain text files into asset tags
            if parsed_data["type"] == "text":
                text_manifests.append(
                    f'<asset path="{abs_path}" type="text">\n'
                    f"{parsed_data['content']}\n"
                    f"</asset>\n"
                )
                
            # Bundles imgs into list and then indexs them
            elif parsed_data["type"] == "image":
                img_path = parsed_data["content"]
                global_images.append(img_path)
                text_manifests.append(
                    f'<asset path="{abs_path}" type="image" visual_index="{len(global_images) - 1}">\n'
                    f"[Visual reference asset linked to input image buffer stream]\n"
                    f"</asset>\n"
                )
                
            # Goes through PDF pages and combines each page into the list
            elif parsed_data["type"] == "pdf_images":
                pdf_manifest = f'<asset path="{abs_path}" type="pdf_sequence">\n'
                for idx, img_path in enumerate(parsed_data["content"]):
                    global_images.append(img_path)
                    pdf_manifest += f'  <page number="{idx + 1}" visual_index="{len(global_images) - 1}"/>\n'
                pdf_manifest += f"</asset>\n"
                text_manifests.append(pdf_manifest)

        except ValueError as e:
            print(f"Skipping file {file_path.name}: {e}", file=sys.stderr)

    return "\n".join(text_manifests)


def main():
    make_dirs()
    print("Launching InferR...")

    # Just makes sure instructions are properly loaded
    try:
        system_instructions = load_sys_prompt()
        context_layout = load_context_layout()
    except Exception as e:
        print(f"Initialization Error: {e}")
        return

    all_execution_images = []

    print("Reading instruction set(s)...")
    instruction_text = process_folder(INSTRUCTIONS_RAW, INSTRUCTIONS_PARSED, all_execution_images)

    print("Reading problem set(s)...")
    problem_text = process_folder(PROBLEMS_RAW, PROBLEMS_PARSED, all_execution_images)

    if not problem_text and not all_execution_images:
        print("Error: No problem assets detected in data/problems/raw/.")
        return

    instruction_assets = instruction_text if instruction_text else "No instruction assets provided."
    problem_assets = problem_text if problem_text else "No problem assets provided."

    payload = context_layout.format(instruction_assets=instruction_assets, problem_assets=problem_assets)
    final_prompt = f"{system_instructions}\n\n{payload}"

    print(f"Files are loaded. Total images analyzed by InferR: {len(all_execution_images)}")
    print("Passing the payload to the Ollama model...")

    try:
        result = query_model(prompt=final_prompt, images=all_execution_images)
        
        print("\n================ INFERR RAN SUCCESSFULLY ================")
        print(json.dumps(result, indent=2))
        
        output_file = OUTPUT_DIR / "execution_output.json"
        output_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"\nJSON output saved to: {output_file}")
        
        pdf_file = OUTPUT_DIR / "execution_report.pdf"
        generate_pdf_report(result, pdf_file)
        print(f"PDF output saved at: {pdf_file}")
        
    except Exception as e:
        print(f"\nInferR Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
