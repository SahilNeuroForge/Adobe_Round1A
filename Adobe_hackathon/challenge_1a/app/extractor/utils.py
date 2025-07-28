# extractor/utils.py

import re
import unicodedata

def clean_text(text: str) -> str:
    """
    Cleans up extracted text. Normalizes unicode, punctuation, and whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFKC', text)
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-")
    return re.sub(r'\s+', ' ', text).strip()

def clean_metadata_title(text: str) -> str:
    """
    Performs aggressive cleaning on a title string, typically from PDF metadata.
    Removes common prefixes, file extensions, and other noise.
    """
    if not text:
        return ""
    
    # Remove common prefixes from software
    text = re.sub(r'^(Microsoft Word - |Adobe Acrobat - )', '', text, flags=re.IGNORECASE)
    
    # Remove file extensions
    text = re.sub(r'\.(pdf|docx?|pptx?|xlsx?|doc|cdr)$', '', text, flags=re.IGNORECASE)
    
    # Remove versioning or date codes that look like V01 or 20161003
    text = re.sub(r'\s*V\d{1,2}\s*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*\d{8}\s*$', '', text)
    
    return clean_text(text)

def reconstruct_line_text(line: dict) -> str:
    """
    Intelligently reconstructs text from a line's spans, accounting for
    spacing based on character coordinates to fix fragmentation.
    """
    spans = line.get("spans", [])
    if not spans:
        return ""
    
    spans.sort(key=lambda s: s['bbox'][0]) # Sort spans by horizontal position
    full_text = ""
    last_x1 = spans[0]['bbox'][0] # Initialize with the start of the first span

    for span in spans:
        current_x0 = span['bbox'][0]
        # Add a space if the gap between spans is larger than a small threshold
        if current_x0 > last_x1 + 1.0:
            full_text += " "
        
        full_text += span['text']
        last_x1 = span['bbox'][2]
        
    return clean_text(full_text)