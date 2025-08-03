import os
import json
from jd_dataExtractor import extract_structured_info_groq_jd  # Assuming you've saved that function in this module

def read_text_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    jd_path = r"C:\Users\User\.vscode\PYTHON PRACTICE\InfoOrigin-Internship\ResumeMatching\jd.txt"  # Make sure this is the correct path to your JD file

    if not os.path.exists(jd_path):
        print(f"❌ File not found: {jd_path}")
        return

    jd_text = read_text_file(jd_path)

    print("📡 Sending JD to Groq for metadata extraction...\n")
    metadata = extract_structured_info_groq_jd(jd_text)

    if metadata:
        print("✅ Extracted Job Description Metadata:\n")
        print(json.dumps(metadata, indent=2)) 
    else:
        print("❌ Failed to extract structured metadata.")

if __name__ == "__main__":
    main()
