import os
from filterMatcher import find_matching_resumes
from jd_dataExtractor import extract_structured_info_groq_jd
from saveFiltered import save_matches_to_json


def load_jd(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    jd_path = r"C:\Users\User\.vscode\PYTHON PRACTICE\InfoOrigin-Internship\ResumeMatching\jd.txt"

    if not os.path.exists(jd_path):
        print(f"❌ File not found: {jd_path}")
        return

    jd_text = load_jd(jd_path)

    print("📡 Sending JD to Groq for metadata extraction...\n")
    metadata = extract_structured_info_groq_jd(jd_text)

    if metadata:
        print("✅ Extracted Job Description Metadata:\n")        
        # find_matching_resumes(jd_text)
        matches = find_matching_resumes(jd_text)
        save_matches_to_json(matches, jd_info=metadata)
        
    else:
        print("❌ Failed to extract structured metadata.")

if __name__ == "__main__":
    main()
