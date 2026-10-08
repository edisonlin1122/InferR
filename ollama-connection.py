import argparse
from parser import parse_file
import ollama

def query_file(file_path, model_name="qwen3.5:9b"):
    print(f"Processing file: {file_path}")

    try:
        parsed_data = parse_file(file_path)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return

    if parsed_data["type"] == "text":
        file_text = parsed_data["content"]

        if not file_text:
            print("File is empty or contains no text.")
            return
        print(f"Sending data to Ollama model {model_name}")

        prompt = f"Analyze the following data: {file_text}" #change

        try:
            response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
            print(response["message"]["content"])
        except Exception as e:
            print(f"Error querying Ollama: {e}")
            print("Ensure connection of Ollama is established.")

    #elif parsed_data["type"] == "image":
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Ollama with file type")
    parser.add_argument("path", help="The path to the file...(.txt, .png, .jpg, .pdf, etc.)")
    parser.add_argument("--model", default="qwen3.5:9b", help="The Ollama model to use.")

    args = parser.parse_args()
    query_file(args.path, args.model)

