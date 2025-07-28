# challenge_1b/analyzer/persona_matcher.py
from sentence_transformers import SentenceTransformer, util
import fitz
from pathlib import Path

model = SentenceTransformer("all-MiniLM-L6-v2")  # ~80MB

def find_relevant_sections(pdf_path, persona, job):
    doc = fitz.open(pdf_path)
    results = []
    query = f"{persona}. {job}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    for page_num, page in enumerate(doc):
        text = page.get_text()
        if not text.strip():
            continue
        page_embedding = model.encode(text, convert_to_tensor=True)
        score = util.pytorch_cos_sim(query_embedding, page_embedding)[0][0].item()

        if score > 0.4:
            results.append({
                "text": text,
                "page_number": page_num + 1,
                "score": round(score, 3),
                "section_title": text.split("\n")[0][:50],
                "document": Path(pdf_path).name
            })

    doc.close()
    return results
