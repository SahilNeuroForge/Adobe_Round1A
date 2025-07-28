# Challenge 1a: PDF Title Extraction

## Overview
This project extracts the title from PDF documents using a combination of metadata analysis and robust heuristics. It is designed for the Adobe Hackathon and demonstrates document analysis using Python and PyMuPDF (fitz).

## Folder Structure
```
challenge_1a/
├── Dockerfile
├── README.md
├── app/
│   ├── main.py
│   ├── extractor/
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── heading_extractor.py
│   │   ├── title_extractor.py
│   │   ├── utils.py
│   │   └── __pycache__/
│   ├── input/
│   │   ├── file01.pdf
│   │   ├── file02.pdf
│   │   └── ...
│   └── output/
│       ├── file01.json
│       ├── file02.json
│       └── ...
└── output/
```

## Features
- Extracts document titles using PDF metadata and text heuristics
- Cleans and normalizes extracted titles
- Outputs results in JSON format
- Dockerized for easy deployment

## Requirements
- Python 3.10+
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)
- Other dependencies as specified in your Dockerfile

## Setup
### 1. Clone the repository
```powershell
# Replace with your repo URL
git clone <repo-url>
cd challenge_1a
```

### 2. Install dependencies
You can use Docker or install Python packages manually.

#### Using Docker
```powershell
docker build -t pdf-title-extractor .
docker run --rm -v ${PWD}/app/input:/app/input -v ${PWD}/app/output:/app/output pdf-title-extractor
```

#### Manual Python Setup
```powershell
pip install pymupdf
```

## Usage
### 1. Place PDF files in the `app/input/` directory.

### 2. Run the extraction script
```powershell
python app/main.py
```

### 3. Output
Extracted titles will be saved as JSON files in `app/output/`, e.g.:
```json
{
  "filename": "file01.pdf",
  "title": "South of France - Cities"
}
```

## Example
Suppose you have a PDF named `file01.pdf` in `app/input/`.
After running the script, you will find `file01.json` in `app/output/` containing the extracted title.

## How It Works
- The script first checks the PDF metadata for a title.
- If the metadata is unreliable or missing, it analyzes the first page's text blocks, scoring them by font size, boldness, and position to find the most likely title.
- The result is cleaned and saved in a JSON file.

## Customization
- You can adjust the heuristics in `app/extractor/title_extractor.py` for different document layouts.
- Input/output paths can be changed in `main.py`.

## Troubleshooting
- If extraction fails, check that your PDFs are not encrypted and are readable by PyMuPDF.
- Errors will be printed to the console for debugging.

## License
This project is for educational and hackathon use only.



# Challenge 1b: Persona-Based PDF Summarization

## Overview
This project summarizes PDF documents and matches content to user personas using custom analysis and summarization logic. It is designed for the Adobe Hackathon and demonstrates advanced document processing and persona matching in Python.

## Folder Structure
```
challenge_1b/
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
├── analyzer/
│   ├── __init__.py
│   ├── persona_matcher.py
│   ├── summarizer.py
│   └── __pycache__/
├── collections/
│   ├── Collection 1/
│   │   ├── 1b_output.json
│   │   ├── challenge1b_input.json
│   │   ├── challenge1b_output.json
│   │   └── PDFs/
│   │       ├── South of France - Cities.pdf
│   │       ├── ...
│   ├── Collection 2/
│   │   ├── 1b_output.json
│   │   ├── challenge1b_input.json
│   │   ├── challenge1b_output.json
│   │   └── PDFs/
│   │       ├── Learn Acrobat - Create and Convert_1.pdf
│   │       ├── ...
│   └── Collection 3/
│       ├── ...
```

## Features
- Summarizes PDF content for different user personas
- Matches document sections to persona interests
- Outputs results in JSON format for each collection
- Dockerized for easy deployment

## Requirements
- Python 3.10+
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)
- Other dependencies as specified in `requirements.txt` and your Dockerfile

## Setup
### 1. Clone the repository
```powershell
# Replace with your repo URL
git clone <repo-url>
cd challenge_1b
```

### 2. Install dependencies
You can use Docker or install Python packages manually.

#### Using Docker
```powershell
docker build -t pdf-persona-summarizer .
docker run --rm -v ${PWD}/collections:/app/collections pdf-persona-summarizer
```

#### Manual Python Setup
```powershell
pip install -r requirements.txt
```

## Usage
### 1. Place PDF files in the appropriate `collections/Collection X/PDFs/` directory.
### 2. Prepare persona input files (e.g., `challenge1b_input.json`).
### 3. Run the summarization script
```powershell
python main.py
```

### 4. Output
Summarized and persona-matched results will be saved as JSON files in each collection folder, e.g.:
```json
{
  "persona": "Business Traveler",
  "summary": "This PDF covers hotels, restaurants, and travel tips for business visitors."
}
```

## Example
Suppose you have a persona input file and several PDFs in `collections/Collection 1/PDFs/`.
After running the script, you will find `1b_output.json` in the same collection folder containing summaries matched to each persona.

## How It Works
- The script loads persona definitions from input JSON files.
- It analyzes each PDF, extracting relevant sections and summarizing content.
- It matches summaries to personas based on keywords and interests.
- Results are saved in output JSON files for each collection.

## Customization
- You can adjust persona definitions in the input JSON files.
- Summarization and matching logic can be modified in `analyzer/persona_matcher.py` and `analyzer/summarizer.py`.
- Input/output paths can be changed in `main.py`.

## Troubleshooting
- Ensure PDFs are readable and not encrypted.
- Check that persona input files are correctly formatted JSON.
- Errors will be printed to the console for debugging.

## License
This project is for educational and hackathon use only.

---

# Challenge 1a: PDF Title Extraction

## Overview
This project extracts the title from PDF documents using a combination of metadata analysis and robust heuristics. It is designed for the Adobe Hackathon and demonstrates document analysis using Python and PyMuPDF (fitz).

## Folder Structure
```
challenge_1a/
├── Dockerfile
├── README.md
├── app/
│   ├── main.py
│   ├── extractor/
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── heading_extractor.py
│   │   ├── title_extractor.py
│   │   ├── utils.py
│   │   └── __pycache__/
│   ├── input/
│   │   ├── file01.pdf
│   │   ├── file02.pdf
│   │   └── ...
│   └── output/
│       ├── file01.json
│       ├── file02.json
│       └── ...
└── output/
```

## Features
- Extracts document titles using PDF metadata and text heuristics
- Cleans and normalizes extracted titles
- Outputs results in JSON format
- Dockerized for easy deployment

## Requirements
- Python 3.10+
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)
- Other dependencies as specified in your Dockerfile

## Setup
### 1. Clone the repository
```powershell
# Replace with your repo URL
git clone <repo-url>
cd challenge_1a
```

### 2. Install dependencies
You can use Docker or install Python packages manually.

#### Using Docker
```powershell
docker build -t pdf-title-extractor .
docker run --rm -v ${PWD}/app/input:/app/input -v ${PWD}/app/output:/app/output pdf-title-extractor
```

#### Manual Python Setup
```powershell
pip install pymupdf
```

## Usage
### 1. Place PDF files in the `app/input/` directory.

### 2. Run the extraction script
```powershell
python app/main.py
```

### 3. Output
Extracted titles will be saved as JSON files in `app/output/`, e.g.:
```json
{
  "filename": "file01.pdf",
  "title": "South of France - Cities"
}
```

## Example
Suppose you have a PDF named `file01.pdf` in `app/input/`.
After running the script, you will find `file01.json` in `app/output/` containing the extracted title.

## How It Works
- The script first checks the PDF metadata for a title.
- If the metadata is unreliable or missing, it analyzes the first page's text blocks, scoring them by font size, boldness, and position to find the most likely title.
- The result is cleaned and saved in a JSON file.

## Customization
- You can adjust the heuristics in `app/extractor/title_extractor.py` for different document layouts.
- Input/output paths can be changed in `main.py`.

## Troubleshooting
- If extraction fails, check that your PDFs are not encrypted and are readable by PyMuPDF.
- Errors will be printed to the console for debugging.

## License
This project is for educational and hackathon use only.
