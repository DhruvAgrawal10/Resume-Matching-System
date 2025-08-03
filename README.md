
# 📄 Resume Matching System (AI-Powered Candidate Filtering)

A scalable, real-world-ready **Resume Matching System** that intelligently parses, filters, and ranks resumes based on job descriptions using **NLP**, **LLMs**, and **semantic embeddings**. Designed for bulk hiring use cases with a modular pipeline structure.

## 📌 Key Features

- 🧠 **JD parsing using Groq’s LLaMA3 model**
- 📄 **Resume parsing from `.pdf` and `.docx` files**
- 🔖 **Canonical job role tagging (`jobtitle_flag`)**
- 🗺️ **Location-aware filtering: State → Neighboring States → Country**
- 💼 **Filtering on `jobtitle_flag` and `job_title`**
- 📦 **Result export as structured `.json` files**
- 🔍 **Embeddings via `intfloat/e5-base` and `JobBERT`**
- 💽 **PostgreSQL + pgvector backend**
- 🚀 **No scoring in filtering step — boolean-only for clarity**
- 🧩 **Pluggable matching and ranking logic**
- 🌐 **Supports Indian and international geographies**

## 🗃️ Directory Structure

```
ResumeMatching/
│
├── resumeExtractor.py         # Resume metadata extractor
├── jd_dataExtractor.py        # JD metadata extractor (via Groq)
├── filterMatcher.py           # Filtering logic using job title, location
├── saveFiltered.py            # Save filtered results as JSON
├── match_driver.py            # Entry point for matching pipeline
├── jobbert_matcher.py         # Embedding-based job title matcher
├── Neighbours.py              # Country-wise state → neighbors dictionary
│
├── resumes/                   # Raw resume uploads
├── results/                   # Output JSON files
├── jd_samples/                # JD text files for testing
├── requirements.txt
└── README.md
```

## 🧠 Pipeline Overview

### Step 1️⃣: Resume Metadata Extraction (One-Time)
- Extract name, job title, skills, experience, education, country/state
- Clean full resume text (`inline_resume`)
- Auto-classify `jobtitle_flag` using JobBERT
- Embedding vector stored via pgvector

### Step 2️⃣: Job Description Parsing (Groq)
- Groq's LLM extracts:
  - `job_title`, `jobtitle_flag`
  - `required_skills`, `required_education`, `required_experience`
  - `state`, `country` (location constraints)

### Step 3️⃣: Resume Filtering (Boolean Logic)
- **Phase 1**: Strict match on `state + country`
- **Phase 2**: Neighboring states fallback (via `Neighbours.py`)
- **Phase 3**: Entire country fallback if candidates < threshold
- Filtering requires matching jobtitle flag or job title

### Step 4️⃣: Result Saving & Display
- Distinguishes candidates:
  - ✅ Strict Match
  - 🟡 Neighbor State Match
  - 🟠 Country Match
- Results saved to `/results/{jd_title}_{timestamp}.json`

## 📦 Sample JSON Output

```json
[
  {
    "name": "Rohan Desai",
    "job_title": "Data Scientist",
    "jobtitle_flag": "Data & AI Professional",
    "state": "Maharashtra",
    "country": "India",
    "location_match": false,
    "date_uploaded": "2025-07-15T05:44:45.727177"
  }
]
```

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/yourusername/resume-matching-system.git
cd resume-matching-system
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ PostgreSQL Setup
Ensure PostgreSQL is installed and running.

```sql
CREATE DATABASE ResumeDB;

-- Create resume table with vector storage
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE resume (
    id SERIAL PRIMARY KEY,
    name TEXT,
    job_title TEXT,
    jobtitle_flag TEXT,
    skills TEXT,
    experience TEXT,
    education TEXT,
    country TEXT,
    state TEXT,
    upload_date TIMESTAMP,
    inline_resume TEXT,
    embedding VECTOR(768)
);
```

### 4️⃣ Set API Key
Set your Groq API key and model in `jd_dataExtractor.py` or `.env`:

```python
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "llama3-70b-8192"
```

## ▶️ How to Run

### Match resumes with a JD:

1. Add a JD file (`jd.txt`)
2. Run the driver:

```bash
python match_driver.py
```

It will:
- Extract structured JD
- Find matching resumes
- Print matches
- Save filtered results to `results/` as `.json`

## 🧠 Matching Logic Summary

| Phase      | Match Scope        | Priority | Notes                                  |
|------------|--------------------|----------|----------------------------------------|
| Phase 1    | Exact State + Country | ✅ Strict | Direct matches only                    |
| Phase 2    | Neighboring States     | 🟡 Soft   | Fallback using country-specific dict   |
| Phase 3    | Entire Country         | 🟠 Softest | Final fallback for broader coverage    |

## 🧱 Tech Stack

- **Python 3.10+**
- **PostgreSQL** + `pgvector`
- **Sentence Transformers** (`e5-base`, `JobBERT`)
- **Langchain (optional)** for prompt chaining
- **Groq API** (LLaMA3 models)
- **pdfminer / python-docx** for resume parsing

## 🔮 Future Enhancements

- [ ] Ranking engine (cosine similarity + scoring)
- [ ] LangChain + RAG for interactive JD clarification
- [ ] Resume upload UI (Streamlit / Flask)
- [ ] Advanced analytics dashboard
- [ ] Feedback-driven retraining (active learning)

## 🧪 Testing

Use `match_driver.py` to run the entire pipeline on a sample JD.
Ensure resume metadata is pre-extracted and stored in PostgreSQL.

## 💡 Contribution Guide

We welcome contributions! If you'd like to:
- Add new JD formats
- Improve metadata extraction
- Extend filtering logic
- Build a frontend

Feel free to fork, open PRs, or raise issues.

## 📜 License

MIT License. See `LICENSE` for full terms.

## 👨‍💻 Author

**Dhruv Kumar Agrawal**  
Intern @ InfoOrigin | AI/ML, NLP, LLMs & Systems Design

## ⭐ Support the Project

If this project helped you, consider giving it a ⭐ on GitHub and sharing your feedback!
