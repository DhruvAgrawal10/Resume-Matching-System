from Matcher import find_filtered_matching_resumes

def load_jd(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    JD_FILE = r"C:\Users\User\.vscode\PYTHON PRACTICE\InfoOrigin-Internship\ResumeMatching\jd.txt"  
    jd_text = load_jd(JD_FILE)

    

    find_filtered_matching_resumes(
        jd_text=jd_text,
        job_title_filter="Java Developer",
        
    )
