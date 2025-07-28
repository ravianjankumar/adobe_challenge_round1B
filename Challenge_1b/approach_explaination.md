## Round 1B: Approach Explanation – Persona-Driven Document Intelligence

### Objective
To extract and rank the most relevant document sections and sub-sections based on a provided persona and their job-to-be-done, using a lightweight and efficient NLP-based approach that runs offline in under 60 seconds on CPU-only hardware.

### 1. Preprocessing
Each collection folder (Collection 1, 2, 3, etc.) includes:
- `input.json`: defines the persona, job-to-be-done, and relevant PDFs
- `PDFs/`: contains all referenced PDFs for analysis

The system reads each PDF using `pdfplumber`, and splits each page into clean, newline-separated paragraphs (skipping short or irrelevant fragments).

### 2. Semantic Scoring using TF-IDF
To assess relevance:
- We construct a text corpus including the job-to-be-done and all paragraph chunks extracted from the PDFs.
- Using `TfidfVectorizer` from `scikit-learn`, we compute feature vectors for each text snippet.
- We apply cosine similarity between the job-to-be-done and each paragraph to score its relevance.

This enables fast, interpretable section scoring with no large pretrained models, keeping memory and execution time minimal.

### 3. Section & Sub-section Extraction
The top 5 scoring sections are selected for output. Each is included:
- Once in the `extracted_sections` list (with title, rank, page number)
- Again in the `subsection_analysis` with the full paragraph text and page reference

The rank is determined by descending TF-IDF similarity score.

### 4. Output Generation
The solution writes a compliant `challenge1b_output.json` to the same folder as the input, including:
- Metadata (persona, job, timestamp)
- Extracted section info with importance rank
- Subsection analysis with raw content

### 5. Offline Compliance
- The system does not use any internet connection.
- It runs entirely on CPU with lightweight libraries: `pdfplumber`, `scikit-learn`, `numpy`.
- Model size is negligible, staying well below the 1GB constraint.

### Conclusion
This approach prioritizes generalizability and speed by using efficient statistical methods and interpretable scores. It supports various personas and domains by working on semantic text similarity without hand-coded rules or templates.
