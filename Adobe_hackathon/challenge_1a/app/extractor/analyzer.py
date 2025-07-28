# extractor/analyzer.py

import fitz

def classify_document(doc: fitz.Document) -> str:
    """
    Analyzes a document's layout and content to classify it into a general type.
    This version is hardened against errors and uses more robust heuristics.
    """
    if not doc or doc.is_closed or len(doc) == 0:
        return "FORMAL_DOCUMENT"  # Default for safety

    first_page = doc[0]
    
    # --- Safe text access ---
    page_text_lower = first_page.get_text("text").lower()

    # --- Heuristic 1: Check for Forms ---
    form_keywords = ["application form", "registration form", "declaration", "undertake", "signature", "date of birth"]
    # The presence of tables and form keywords is a very strong indicator.
    if any(keyword in page_text_lower for keyword in form_keywords):
        if first_page.find_tables().tables:
            return "FORM"

    # --- Heuristic 2: Check for Graphical Flyers/Invitations ---
    # Flyers are typically single-page, image-heavy, with stylistic fonts.
    if len(doc) == 1:
        word_count = len(first_page.get_text("words"))
        image_count = len(first_page.get_images(full=True))
        
        unique_font_sizes = set()
        try:
            for block in first_page.get_text("dict").get("blocks", []):
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        unique_font_sizes.add(round(span.get("size", 0)))
        except:
            pass # Ignore parsing errors

        # High font variety, low word count, and presence of images suggest a flyer.
        if word_count < 400 and len(unique_font_sizes) > 5 and image_count > 0:
            return "GRAPHICAL_FLYER"

    # --- Heuristic 3 & Default: Formal Documents ---
    # Multi-page documents, or those with a ToC, are almost always formal.
    if len(doc) > 1 or doc.get_toc():
        return "FORMAL_DOCUMENT"

    return "FORMAL_DOCUMENT"  # Default classification