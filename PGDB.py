import psycopg2
from sentence_transformers import SentenceTransformer
from psycopg2.extras import Json
import hashlib

DB_CONFIG = {
    "dbname": "ResumeDB",
    "user": "postgres",
    "password": "mysecretpassword",
    "host": "localhost",
    "port": 5433
}

model = SentenceTransformer("intfloat/e5-base")

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_embedding(text):
    return model.encode(text).tolist()

def compute_file_hash(text):
    sha256 = hashlib.sha256()
    sha256.update(text.strip().encode('utf-8'))
    return sha256.hexdigest()

def check_hash_exists(conn, file_hash):
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM resume WHERE file_hash = %s", (file_hash,))
        return cur.fetchone() is not None

def insert_resume_into_db(conn, structured_info, cleaned_text,file_hash):
    try:
        
        file_hash = compute_file_hash(cleaned_text)        

        with conn.cursor() as cur:
            
            # Check for existing resume by hash
            cur.execute("SELECT 1 FROM resume WHERE file_hash = %s", (file_hash,))
            if cur.fetchone():
                print("❌ Duplicate resume (same file hash) — skipping insert.")
                return
            
            skills_array = structured_info.get("skills") or []

            cur.execute("""
                INSERT INTO resume (
                    name, state , state_embedding , country, country_embedding ,
                    job_title, job_title_embedding , jobtitle_flag , jobtitle_flag_embedding ,
                    skills, skills_embedding , experience , years_of_relevant_experience, education,
                    inline_resume, resume_embedding,file_hash,total_yrs_of_exp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                structured_info.get("name"),
                structured_info.get("state") or "Not Specified",
                get_embedding(structured_info.get("state") or "Not Specified"),
                structured_info.get("country") or "Not Specified",
                get_embedding(structured_info.get("country") or "Not Specified"),
                structured_info.get("job_title") or "Not Specified",
                get_embedding(structured_info.get("job_title") or "Not Specified"),
                structured_info.get("jobtitle_flag") or "Not Specified",
                get_embedding(structured_info.get("jobtitle_flag") or "Not Specified"),
                skills_array,
                get_embedding(" ".join(skills_array)),
                Json(structured_info.get("experience")) ,
                structured_info.get("years_of_relevant_experience") or "Not Specified",
                Json(structured_info.get("education")) ,
                cleaned_text,
                get_embedding(cleaned_text),
                file_hash,
                structured_info.get("total_yrs_of_exp") or "0"
                
                
            ))
        conn.commit()
        
    except Exception as e:
        print(f" Error during DB insert: {e}")
        conn.rollback()
        conn.close() 
        conn = get_db_connection() 
        raise e