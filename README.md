# Challenge 1B: Persona-Driven Document Intelligence

## 🔍 Overview
This project solves Adobe Hackathon Round 1B: Extract and prioritize relevant information from PDFs for a given persona and job-to-be-done. The system reads a collection of PDFs, processes them based on the persona/task context, and outputs structured JSON highlighting relevant sections.

## 🧠 Key Features
- Handles multiple collections (`Collection 1`, `Collection 2`, etc.)
- Extracts top 5 relevant sections from PDFs
- Outputs results in `challenge1b_output.json`
- Runs 100% offline on CPU (≤60s, ≤1GB)

## 📁 Folder Structure
Challenge_1b/
├── main.py
├── Dockerfile
├── requirements.txt
├── Collection 1/
│ ├── input.json
│ ├── PDFs/
│ └── challenge1b_output.json
├── Collection 2/
│ └── ...
├── Collection 3/
│ └── ...

## ⚙️ How It Works
1. `input.json` defines:
   - persona
   - job to be done
   - list of document filenames
2. All PDFs should be in `PDFs/`
3. `main.py` uses TF-IDF + cosine similarity to rank relevance
4. Outputs top 5 ranked paragraphs as sections + analysis

## 🚀 Running the Solution
### 🔧 Install dependencies (for local run)

```bash
pip install -r requirements.txt

python main.py

docker build --platform linux/amd64 -t round1b-solution .

docker run --rm -v $(pwd):/app round1b-solution
