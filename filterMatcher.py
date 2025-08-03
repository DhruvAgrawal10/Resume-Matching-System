import psycopg2
import json,re,requests
import numpy as np
from sentence_transformers import SentenceTransformer
from Neighbours import neighbors_data
from jd_dataExtractor import extract_structured_info_groq_jd
from sklearn.metrics.pairwise import cosine_similarity
import ast

DB_CONFIG = {
    "dbname": "ResumeDB",
    "user": "postgres",
    "password": "mysecretpassword",
    "host": "localhost",
    "port": 5433
}

GROQ_API_KEY = ""
GROQ_MODEL = "llama3-70b-8192"

model = SentenceTransformer("intfloat/e5-base")

def parse_embedding(emb):
    if emb is None:
        return np.array([])
    if isinstance(emb, (list, np.ndarray)):
        return np.array(emb)
    if isinstance(emb, str):
        try:
            return np.array(ast.literal_eval(emb))
        except Exception:
            return np.array([])
    return np.array([])

def safe_text(x):
    """
    Return a clean string for embedding.
    - None   →  ""   (empty string)
    - list   →  ", ".join(str(e) for e in x if e)
    - other  →  str(x)
    """
    if x is None:
        return ""
    if isinstance(x, list):
        return ", ".join(str(e) for e in x if e)
    return str(x)

def get_neighboring_states_dict(target_state: str) -> list[str]:
    target_state = target_state.strip().title()

    if not target_state or target_state.lower() == "remote":
        return []

    return neighbors_data.get(target_state, [])


# def extract_years_from_string(s):
#     try:
#         match = re.search(r"\d+", str(s))
#         return int(match.group()) if match else 0
#     except:
#         return 0

def create_jd_embedding(jd_text):
    jd_structured = extract_structured_info_groq_jd(jd_text)
    if jd_structured is None:
        raise ValueError("Could not extract structured JD metadata.")

    jd_resume_like = {
        "job_title": jd_structured.get("job_title", ""),
        "jobtitle_flag": jd_structured.get("jobtitle_flag") ,
        "skills": jd_structured.get("required_skills", []),
        "experience": [{"title": jd_structured.get("required_experience", "")}],
        "education": [{"degree": jd_structured.get("required_education", "")}]
    }

    embeddings = {
        "jobtitle_flag": model.encode(safe_text(jd_resume_like["jobtitle_flag"])),
        "skills":        model.encode(safe_text(jd_resume_like["skills"])),
        "experience":    model.encode(safe_text(jd_resume_like["experience"][0]["title"])),
        "education":     model.encode(safe_text(jd_resume_like["education"][0]["degree"]))
    }
    return jd_structured, embeddings

def find_matching_resumes(jd_text, top_n=5, date_filter_days=730,needed_local=5):
    jd_structured, jd_embeddings = create_jd_embedding(jd_text)
    
    jd_state   = (jd_structured.get("state")   or "").strip().title()
    jd_country = (jd_structured.get("country") or "").strip().title()
    jd_flag   = (jd_structured.get("jobtitle_flag") or "").strip().lower()
    jd_title = (jd_structured.get("job_title") or "").strip().lower()
    neighbours = []

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(f"""
        SELECT id, name, job_title, jobtitle_flag, skills, experience, education,
               country, state, upload_date
        FROM resume
        WHERE upload_date >= CURRENT_DATE - INTERVAL '{date_filter_days} days'
    """)

    rows = cur.fetchall()
    conn.close()
    
    def is_location_match(state, country, target_state, target_country):
        if target_state.lower() == "remote" or target_country.lower() == "remote":
            return True
        return (
            (state and state.strip().title() == target_state) and
            (country and country.strip().title() == target_country)
        )

    
        
    # Phase 1: Filter strictly by specified location
    filtered = [
        {
            "id": id,
            "name": name,
            "job_title": job_title,
            "jobtitle_flag": jobtitle_flag,
            "skills": skills,
            "experience": experience,
            "education": education,
            "country": country,
            "state": state,
            "date_uploaded": date_uploaded,
            "match_level": "strict"
        }
        for (id, name, job_title, jobtitle_flag, skills, experience, education,
             country, state, date_uploaded) in rows
        if is_location_match(state, country, jd_state, jd_country) and(
            (jobtitle_flag and jobtitle_flag.strip().lower() == jd_flag ) or 
            (job_title and job_title.strip().lower() == jd_title)
        )
        
    ]

    # Phase 2: Expand to neighboring states if fewer than 5 candidates found
    if len(filtered) <needed_local and jd_state.lower() not in ["", "remote"]:
        neighbors = get_neighboring_states_dict(jd_state)
        neighbor_filtered = [
            {
                "id": id,
                "name": name,
                "job_title": job_title,
                "jobtitle_flag": jobtitle_flag,
                "skills": skills,
                "experience": experience,
                "education": education,
                "country": country,
                "state": state,
                "date_uploaded": date_uploaded,
                "match_level": "neighbor"
            }
            for (id, name, job_title, jobtitle_flag, skills, experience, education,
                 country, state, date_uploaded) in rows
            if state and state.strip().title() in neighbors and(
                (jobtitle_flag and jobtitle_flag.strip().lower() == jd_flag ) or 
                (job_title and job_title.strip().lower() == jd_title)
            ) and not any(existing["id"] == id for existing in filtered)
        ]
        filtered += neighbor_filtered
        
   # Phase 3: If still fewer than 5, filter by country
    if len(filtered) <needed_local and jd_country.lower() not in ["", "remote"]:
        country_filtered = [
            {
                "id": id,
                "name": name,
                "job_title": job_title,
                "jobtitle_flag": jobtitle_flag,
                "skills": skills,
                "experience": experience,
                "education": education,
                "country": country,
                "state": state,
                "date_uploaded": date_uploaded,
                "match_level": "country"
            }
            for (id, name, job_title, jobtitle_flag, skills, experience, education,
                country, state, date_uploaded) in rows
            if country and country.strip().title() == jd_country
                and not any(existing["id"] == id for existing in filtered) and(
                (jobtitle_flag and jobtitle_flag.strip().lower() == jd_flag ) or 
                (job_title and job_title.strip().lower() == jd_title)
            )
            
        ]
        filtered += country_filtered       
        
        

        
    for i, r in enumerate(filtered, 1):
        print(f"\n🔹 Candidate #{i}")
        print(f"Name: {r['name']}")
        print(f"Job Title: {r['job_title']}")
        print(f"Canonical Job Role: {r['jobtitle_flag']}")
        print(f"Location: {r['state']}, {r['country']}")
        print(f"Uploaded: {r['date_uploaded']}")
        match_labels = {
            "strict": "✅ Strict Location Match",
            "neighbor": "🟡 Neighboring State",
            "country": "🔴 Country Wide Level"
        }
        print(f"Location Match Type: {match_labels.get(r['match_level'], '❓ Unknown')}")

    return filtered

