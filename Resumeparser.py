import os
import json
import time
from TextExtraction import extract_text
from TextPreprocessing import preprocess_text
from UpdatedMetaDataExtraction2 import extract_resume_metadata
from PGDB import get_db_connection, insert_resume_into_db,compute_file_hash,check_hash_exists



folder = r"C:\Users\User\.vscode\PYTHON PRACTICE\Datasets\NewTestResume"   

def process_all_resumes(folder_path):
    conn = get_db_connection()
    for filename in os.listdir(folder_path):
        if filename.endswith(('.pdf', '.docx', '.doc')):
            full_path = os.path.join(folder_path, filename)
            try:
                text = extract_text(full_path)
                cleaned_text = preprocess_text(text)
                file_hash = compute_file_hash(cleaned_text)

                # ✅ Check hash before metadata extraction
                if check_hash_exists(conn, file_hash):
                    print(f"⛔ Skipping duplicate: {filename}")
                    continue
                
                
                metadata = extract_resume_metadata(cleaned_text)
                print(f"Processed: {filename}")
                # print(json.dumps(metadata, indent=2)) 
                if metadata:
                    insert_resume_into_db(conn, metadata, cleaned_text, file_hash)
                    print(f" Inserted {filename}")
                else:
                    print(f" Skipped {filename} due to extraction failure.")
                time.sleep(3)  
            except Exception as e:
                print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    process_all_resumes(folder)