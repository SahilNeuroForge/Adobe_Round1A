# # challenge_1b/main.py
# import os
# import json
# from analyzer.persona_matcher import find_relevant_sections
# from analyzer.summarizer import summarize

# BASE_DIR = "./collections"
# print("Base directory:", BASE_DIR)

# for collection in os.listdir(BASE_DIR):
#     collection_path = os.path.join(BASE_DIR, collection)
#     if not os.path.isdir(collection_path):
#         continue

#     input_file = os.path.join(collection_path, "challenge1b_input.json")
#     output_file = os.path.join(collection_path, "1b_output.json")
#     pdf_folder = os.path.join(collection_path, "PDFs")

#     if not os.path.exists(input_file) or not os.path.isdir(pdf_folder):
#         print(f"Skipping {collection}: input or PDFs folder missing")
#         continue

#     print(f"Processing: {collection}")
#     with open(input_file, "r", encoding="utf-8") as f:
#         input_data = json.load(f)

#     persona = input_data["persona"]
#     task = input_data["task"]
#     results = []

#     for pdf_file in os.listdir(pdf_folder):
#         if pdf_file.lower().endswith(".pdf"):
#             pdf_path = os.path.join(pdf_folder, pdf_file)
#             print(f"Analyzing: {pdf_file}")
#             sections = find_relevant_sections(pdf_path, persona, task)

#             summarized_sections = []
#             for section in sections:
#                 summary = summarize(section["text"])
#                 summarized_sections.append({
#                     "page_number": section["page_number"],
#                     "section_title": section["section_title"],
#                     "summary": summary,
#                     "score": section["score"]
#                 })

#             results.append({
#                 "file": pdf_file,
#                 "sections": summarized_sections
#             })

#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(results, f, indent=2, ensure_ascii=False)

#     print(f"Output saved to: {output_file}")


import os
import json
import datetime
from analyzer.persona_matcher import find_relevant_sections
from analyzer.summarizer import summarize

BASE_DIR = "./collections"
print("Base directory:", BASE_DIR)

for collection in os.listdir(BASE_DIR):
    collection_path = os.path.join(BASE_DIR, collection)
    if not os.path.isdir(collection_path):
        continue

    input_file = os.path.join(collection_path, "challenge1b_input.json")
    output_file = os.path.join(collection_path, "1b_output.json")
    pdf_folder = os.path.join(collection_path, "PDFs")

    if not os.path.exists(input_file) or not os.path.isdir(pdf_folder):
        print(f"Skipping {collection}: input or PDFs folder missing")
        continue

    print(f"Processing: {collection}")
    with open(input_file, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    # Handle both flat and nested input JSON formats safely
    persona = input_data.get("persona", "")
    if isinstance(persona, dict):
        persona = persona.get("role", "")

    task = input_data.get("task", "")
    if not task:
        task = input_data.get("job_to_be_done", {}).get("task", "")

    timestamp = datetime.datetime.now().isoformat()

    all_input_docs = []
    extracted_sections = []
    subsection_analysis = []

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            all_input_docs.append(pdf_file)
            print(f"Analyzing: {pdf_file}")
            sections = find_relevant_sections(pdf_path, persona, task)

            # Sort by score for ranking
            sections = sorted(sections, key=lambda x: x["score"], reverse=True)

            for rank, section in enumerate(sections, 1):
                extracted_sections.append({
                    "document": section["document"],
                    "page_number": section["page_number"],
                    "section_title": section["section_title"],
                    "importance_rank": rank
                })

                subsection_analysis.append({
                    "document": section["document"],
                    "refined_text": summarize(section["text"]),
                    "page_number": section["page_number"]
                })

    final_output = {
        "metadata": {
            "input_documents": all_input_docs,
            "persona": persona,
            "job": task,
            "timestamp": timestamp
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print(f"Output saved to: {output_file}")
