# extractor/title_extractor.py

import fitz
from .utils import clean_text, clean_metadata_title
from .analyzer import classify_document

def _extract_title_by_heuristic(page: fitz.Page, top_margin: float = 0.4):
    """
    Extracts title by scoring text blocks based on font size, weight, and position.
    """
    candidates = []
    page_height = page.rect.height
    
    blocks = [b for b in page.get_text("dict", sort=True).get("blocks", []) if b['bbox'][1] < page_height * top_margin]
    if not blocks: return "", set()

    for block in blocks:
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans: continue
            
            line_text = clean_text(" ".join(s['text'] for s in spans))
            if not line_text or len(line_text.split()) > 20 or not any(c.isalpha() for c in line_text):
                continue

            span = spans[0]
            font_size = span['size']
            is_bold = "bold" in span['font'].lower()
            y_pos = span['origin'][1]

            score = font_size * 2.0
            if is_bold: score *= 1.2
            score += (page_height - y_pos) / page_height * 5
            
            candidates.append((score, line_text))

    if not candidates: return "", set()
    candidates.sort(key=lambda x: x[0], reverse=True)
    
    # FIX: Return the title string and a set containing the title
    best_title = candidates[0][1]
    return best_title, {best_title}


def extract_title(doc: fitz.Document):
    """
    Extracts the title by checking and cleaning metadata first, then applying
    classification-based rules with a robust heuristic fallback.
    """
    meta_title = doc.metadata.get('title')
    cleaned_title = clean_metadata_title(meta_title)
    
    is_unreliable = '_' in cleaned_title or '  ' in (meta_title or "")
    
    if cleaned_title and len(cleaned_title) > 3 and not is_unreliable:
        # FIX: Return the title string and a set containing the title
        return cleaned_title, {cleaned_title}

    try:
        if doc and not doc.is_closed and len(doc) > 0:
            page = doc[0]
            # FIX: Return the two values from the helper function
            return _extract_title_by_heuristic(page, top_margin=0.4)
    except Exception as e:
        print(f"    -> Warning: Could not extract title due to error: {e}")

    # FIX: Return a tuple with a string and a set, even in the fallback case
    final_title = cleaned_title if cleaned_title else ""
    return final_title, {final_title}