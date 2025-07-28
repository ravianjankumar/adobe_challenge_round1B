import os
import json
import pdfplumber
from pathlib import Path
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
collections = [d for d in BASE_DIR.iterdir() if d.is_dir() and d.name.startswith("Collection")]

for COLLECTION_DIR in collections:
    print(f"\nProcessing {COLLECTION_DIR.name}")
    PDF_DIR = COLLECTION_DIR / "PDFs"
    INPUT_JSON = COLLECTION_DIR / "challenge1b_input.json"
    OUTPUT_JSON = COLLECTION_DIR / "challenge1b_output.json"

    if not INPUT_JSON.exists():
        print(f"Skipping {COLLECTION_DIR.name}: input.json not found.")
        continue

    with open(INPUT_JSON, encoding="utf-8") as f:
        config = json.load(f)

    persona = config["persona"]["role"]
    job = config["job_to_be_done"]["task"]
    document_list = [doc["filename"] for doc in config["documents"]]

    all_chunks = []
    for pdf_file in document_list:
        pdf_path = PDF_DIR / pdf_file
        if not pdf_path.exists():
            print(f"File not found: {pdf_file}")
            continue

        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                for para in text.split("\n"):
                    para = para.strip()
                    if len(para.split()) >= 5:
                        all_chunks.append({
                            "document": pdf_file,
                            "page_number": i + 1,
                            "text": para
                        })

    if not all_chunks:
        print(f"No valid text chunks found in {COLLECTION_DIR.name}.")
        continue

    corpus = [job] + [chunk["text"] for chunk in all_chunks]
    tfidf = TfidfVectorizer().fit_transform(corpus)
    scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    for i, score in enumerate(scores):
        all_chunks[i]["score"] = float(score)

    top_sections = sorted(all_chunks, key=lambda x: -x["score"])[:5]

    output_data = {
        "metadata": {
            "input_documents": document_list,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [
            {
                "document": section["document"],
                "section_title": section["text"][:100],
                "importance_rank": i + 1,
                "page_number": section["page_number"]
            } for i, section in enumerate(top_sections)
        ],
        "subsection_analysis": [
            {
                "document": section["document"],
                "refined_text": section["text"],
                "page_number": section["page_number"]
            } for section in top_sections
        ]
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Output written to {OUTPUT_JSON.name}")
