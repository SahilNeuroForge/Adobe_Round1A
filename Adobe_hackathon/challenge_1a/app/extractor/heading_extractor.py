# extractor/heading_extractor.py

import fitz
import re
from collections import Counter
from .utils import clean_text, reconstruct_line_text
from .analyzer import classify_document

# **FIX**: Blacklist for common non-content headings to be filtered from the outline.
HEADING_BLACKLIST = {
    "table of contents", "contents", "revision history", 
    "acknowledgements", "references", "bibliography", "index", "glossary"
}

def _identify_header_footer_noise(doc: fitz.Document, num_pages_to_check: int = 4) -> set:
    """Identifies repeating text in the top/bottom margins of pages."""
    if doc.page_count <= 2: return set()
    pages_to_scan = min(doc.page_count, num_pages_to_check)
    text_positions = Counter()
    
    for page_num in range(pages_to_scan):
        page = doc.load_page(page_num)
        page_height = page.rect.height
        header_limit, footer_limit = page_height * 0.15, page_height * 0.85
        
        for block in page.get_text("dict").get("blocks", []):
            y0 = block['bbox'][1]
            if y0 < header_limit or y0 > footer_limit:
                for line in block.get("lines", []):
                    line_text = clean_text("".join(s['text'] for s in line.get('spans', [])))
                    if line_text and len(line_text.split()) < 10:
                        text_positions[(line_text, round(y0 / 10))] += 1
                        
    noise_threshold = pages_to_scan // 2 if pages_to_scan > 1 else 1
    return {text for (text, pos), count in text_positions.items() if count >= noise_threshold}


def get_font_profile(doc: fitz.Document):
    """Analyzes font usage across the document."""
    styles = {}
    for page in doc:
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                if line.get("spans"):
                    span = line["spans"][0]
                    style_key = (round(span.get("size", 0)), span.get("font", "default"))
                    styles[style_key] = styles.get(style_key, 0) + len(clean_text("".join(s['text'] for s in line['spans'])))
    return styles

def extract_headings_from_formal_doc(doc: fitz.Document, title: str) -> list:
    """Extracts headings from formal documents, with improved filtering."""
    noise_filter = _identify_header_footer_noise(doc)
    styles = get_font_profile(doc)
    if not styles: return []
    
    body_style = max(styles, key=styles.get, default=None)
    body_size = body_style[0] if body_style else 0
    heading_styles = {s for s in styles if s[0] > body_size + 0.5}
    if not heading_styles: return []

    unique_sizes = sorted(list({s[0] for s in heading_styles}), reverse=True)
    level_map = {size: f"H{i+1}" for i, size in enumerate(unique_sizes)}
    headings, title_lower = [], clean_text(title).lower()

    for page_num, page in enumerate(doc):
        table_bboxes = [fitz.Rect(t.bbox) for t in page.find_tables().tables]
        
        for block in page.get_text("dict").get("blocks", []):
            if any(fitz.Rect(block['bbox']).intersects(t_bbox) for t_bbox in table_bboxes):
                continue
                
            for line in block.get("lines", []):
                if not line.get("spans"): continue
                
                span = line["spans"][0]
                style_key = (round(span.get("size", 0)), span.get("font", "default"))
                
                if style_key in heading_styles:
                    line_text = reconstruct_line_text(line)
                    line_text_lower = line_text.lower()
                    
                    # --- Filtering Rules ---
                    if not line_text or len(line_text.split()) > 20: continue
                    if line_text_lower == title_lower: continue
                    if line_text in noise_filter: continue
                    if line_text_lower in HEADING_BLACKLIST: continue # **FIX**: Filter blacklisted headings
                    if re.match(r'^version\s?[\d\.]+$', line_text_lower): continue # **FIX**: Filter version strings
                    if not any(c.isalpha() for c in line_text): continue
                    
                    headings.append({
                        "level": level_map.get(style_key[0], "H9"),
                        "text": line_text, "page": page_num
                    })
    return headings

def extract_headings(doc: fitz.Document, title: str) -> list:
    """Main router for heading extraction."""
    try:
        toc = doc.get_toc(simple=False)
        if toc:
            title_lower = clean_text(title).lower()
            return [
                {"level": f"H{level}", "text": clean_text(toc_title), "page": page_num - 1}
                for level, toc_title, page_num, *_ in toc
                if clean_text(toc_title).lower() != title_lower and clean_text(toc_title).lower() not in HEADING_BLACKLIST
            ]

        doc_type = classify_document(doc)
        if doc_type == "FORM":
            return []
        if doc_type == "GRAPHICAL_FLYER":
            # Simplified extraction logic for flyers
            return [] 
        if doc_type == "FORMAL_DOCUMENT":
            return extract_headings_from_formal_doc(doc, title)
            
    except Exception as e:
        print(f"    -> Warning: Could not extract headings due to error: {e}")
        
    return []# extractor/heading_extractor.py

import fitz
import re
from collections import Counter
from .utils import clean_text, reconstruct_line_text
from .analyzer import classify_document

# **FIX**: Blacklist for common non-content headings to be filtered from the outline.
HEADING_BLACKLIST = {
    "table of contents", "contents", "revision history", 
    "acknowledgements", "references", "bibliography", "index", "glossary"
}

def _identify_header_footer_noise(doc: fitz.Document, num_pages_to_check: int = 4) -> set:
    """Identifies repeating text in the top/bottom margins of pages."""
    if doc.page_count <= 2: return set()
    pages_to_scan = min(doc.page_count, num_pages_to_check)
    text_positions = Counter()
    
    for page_num in range(pages_to_scan):
        page = doc.load_page(page_num)
        page_height = page.rect.height
        header_limit, footer_limit = page_height * 0.15, page_height * 0.85
        
        for block in page.get_text("dict").get("blocks", []):
            y0 = block['bbox'][1]
            if y0 < header_limit or y0 > footer_limit:
                for line in block.get("lines", []):
                    line_text = clean_text("".join(s['text'] for s in line.get('spans', [])))
                    if line_text and len(line_text.split()) < 10:
                        text_positions[(line_text, round(y0 / 10))] += 1
                        
    noise_threshold = pages_to_scan // 2 if pages_to_scan > 1 else 1
    return {text for (text, pos), count in text_positions.items() if count >= noise_threshold}


def get_font_profile(doc: fitz.Document):
    """Analyzes font usage across the document."""
    styles = {}
    for page in doc:
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                if line.get("spans"):
                    span = line["spans"][0]
                    style_key = (round(span.get("size", 0)), span.get("font", "default"))
                    styles[style_key] = styles.get(style_key, 0) + len(clean_text("".join(s['text'] for s in line['spans'])))
    return styles

def extract_headings_from_formal_doc(doc: fitz.Document, title: str) -> list:
    """Extracts headings from formal documents, with improved filtering."""
    noise_filter = _identify_header_footer_noise(doc)
    styles = get_font_profile(doc)
    if not styles: return []
    
    body_style = max(styles, key=styles.get, default=None)
    body_size = body_style[0] if body_style else 0
    heading_styles = {s for s in styles if s[0] > body_size + 0.5}
    if not heading_styles: return []

    unique_sizes = sorted(list({s[0] for s in heading_styles}), reverse=True)
    level_map = {size: f"H{i+1}" for i, size in enumerate(unique_sizes)}
    headings, title_lower = [], clean_text(title).lower()

    for page_num, page in enumerate(doc):
        table_bboxes = [fitz.Rect(t.bbox) for t in page.find_tables().tables]
        
        for block in page.get_text("dict").get("blocks", []):
            if any(fitz.Rect(block['bbox']).intersects(t_bbox) for t_bbox in table_bboxes):
                continue
                
            for line in block.get("lines", []):
                if not line.get("spans"): continue
                
                span = line["spans"][0]
                style_key = (round(span.get("size", 0)), span.get("font", "default"))
                
                if style_key in heading_styles:
                    line_text = reconstruct_line_text(line)
                    line_text_lower = line_text.lower()
                    
                    # --- Filtering Rules ---
                    if not line_text or len(line_text.split()) > 20: continue
                    if line_text_lower == title_lower: continue
                    if line_text in noise_filter: continue
                    if line_text_lower in HEADING_BLACKLIST: continue # **FIX**: Filter blacklisted headings
                    if re.match(r'^version\s?[\d\.]+$', line_text_lower): continue # **FIX**: Filter version strings
                    if not any(c.isalpha() for c in line_text): continue
                    
                    headings.append({
                        "level": level_map.get(style_key[0], "H9"),
                        "text": line_text, "page": page_num
                    })
    return headings

def extract_headings(doc: fitz.Document, title: str) -> list:
    """Main router for heading extraction."""
    try:
        toc = doc.get_toc(simple=False)
        if toc:
            title_lower = clean_text(title).lower()
            return [
                {"level": f"H{level}", "text": clean_text(toc_title), "page": page_num - 1}
                for level, toc_title, page_num, *_ in toc
                if clean_text(toc_title).lower() != title_lower and clean_text(toc_title).lower() not in HEADING_BLACKLIST
            ]

        doc_type = classify_document(doc)
        if doc_type == "FORM":
            return []
        if doc_type == "GRAPHICAL_FLYER":
            # Simplified extraction logic for flyers
            return [] 
        if doc_type == "FORMAL_DOCUMENT":
            return extract_headings_from_formal_doc(doc, title)
            
    except Exception as e:
        print(f"    -> Warning: Could not extract headings due to error: {e}")
        
    return []