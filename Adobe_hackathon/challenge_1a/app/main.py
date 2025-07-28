import fitz
import json
from pathlib import Path

# The imports for the extractor package now work seamlessly
from extractor.title_extractor import extract_title
from extractor.heading_extractor import extract_headings

def main():
    """Main function to process all PDFs and generate JSON outputs."""
    
    # FIX: Go up one level to find the project's base directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    INPUT_DIR = BASE_DIR / "input"
    OUTPUT_DIR = BASE_DIR / "output"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for pdf_path in INPUT_DIR.glob("*.pdf"):
        print(f"Processing: {pdf_path.name}")
        try:
            with fitz.open(pdf_path) as doc:
                title, title_components = extract_title(doc)
                outline = extract_headings(doc, title_components)

                output_data = {"title": title, "outline": outline}
                out_file = OUTPUT_DIR / f"{pdf_path.stem}.json"

                with open(out_file, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=4, ensure_ascii=False)

                print(f"Successfully saved output to: {out_file}")

        except Exception as e:
            print(f"Could not process {pdf_path.name}. Error: {e}")

if __name__ == "__main__":
    main()