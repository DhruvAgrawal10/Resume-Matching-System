import requests
import json
import re

GROQ_API_KEY = ""
GROQ_MODEL = "llama3-70b-8192"

GROQ_SYSTEM_PROMPT_JD = {
    "role": "system",
    "content": (
        "You are an AI assistant that extracts structured job description (JD) information.\n\n"
        "Return ONLY a single clean JSON object with these fields:\n"
        "- job_title (string)\n"
        "- jobtitle_flag (string): Normalize the extracted job title using fuzzy logic and return a **broad, canonical job category** for filtering\n"
        "    → Use an internal list of 40,000+ known job titles and fuzzy-match variations like:\n"
        "      'Sr. Backend Eng', 'Java Dev', 'ML Ops Lead', 'ERP Func. Consultant', etc.\n"
        "    → Remove seniority terms like 'Senior', 'Lead', 'Principal', 'Jr.', 'Intern' before matching\n"
        "    → Example Business analyst returns Product & Strategy Professional \n"
        "    → Group close variations under a broader flag using these examples:\n\n"
        "Canonical `jobtitle_flag` mappings:\n"
         "- 'Software Developer':\n"
        "    - Software Engineer, Full Stack Developer, Backend Developer, Frontend Developer,\n"
        "      Java Developer, Python Developer, C++ Developer, Mobile App Developer,\n"
        "      iOS Developer, Android Developer, Web Developer, Platform Engineer,\n"
        "      Game Developer, AR/VR Developer, Unity Developer, Embedded Software Engineer,\n"
        "      Application Developer, Systems Developer, Ruby on Rails Developer, Node.js Developer,\n"
        "      Go Developer, Kotlin Developer, Scala Developer, Flutter Developer,\n"
        "      Technical Lead - Software, Senior Developer, Entry Level Software Engineer\n"
        "- 'Data & AI Professional':\n"
        "    - Data Scientist, Machine Learning Engineer, MLOps Engineer, NLP Engineer,\n"
        "      Data Analyst, Data Engineer, Big Data Engineer, Prompt Engineer,\n"
        "      AI Research Scientist, Deep Learning Engineer, Computer Vision Engineer,\n"
        "      Data Architect, Statistical Analyst, AI Specialist, Research Scientist - AI\n"
        "- 'Cloud & DevOps Engineer':\n"
        "    - DevOps Engineer, Site Reliability Engineer, Cloud Architect, Cloud Engineer,\n"
        "      Infrastructure Engineer, CI/CD Engineer, DevSecOps Engineer,\n"
        "      AWS Engineer, Azure Engineer, Google Cloud Engineer, Cloud Consultant\n"
        "- 'ERP & Enterprise Consultant':\n"
        "    - ERP Consultant, SAP Consultant, Oracle ERP Consultant, Workday Consultant,\n"
        "      PeopleSoft Consultant, NetSuite Consultant, JD Edwards Analyst,\n"
        "      Dynamics 365 Consultant, ERP Functional Consultant, ERP Technical Consultant\n"
        "- 'Cybersecurity Specialist':\n"
        "    - Cybersecurity Analyst, Security Engineer, SOC Analyst, Penetration Tester,\n"
        "      Information Security Manager, Red Team Specialist, Application Security Engineer,\n"
        "      Security Architect, Vulnerability Analyst, IAM Specialist, GRC Analyst\n"
        "- 'Product & Strategy Professional':\n"
        "    - Business Analyst, Product Manager, Technical Product Manager, Product Owner, Product Analyst,\n"
        "      Business Strategist, Product Operations Manager,\n"
        "      Business Consultant, Strategy Consultant, Innovation Manager\n"
        "- 'Design & Creative Professional':\n"
        "    - UX Designer, UI Designer, Visual Designer, Motion Designer,\n"
        "      Graphic Designer, Interaction Designer, Creative Director,\n"
        "      Product Designer, Illustrator, Brand Designer, 3D Artist\n"
        "- 'Marketing & Growth Professional':\n"
        "    - Marketing Manager, Content Strategist, SEO Specialist, Social Media Manager,\n"
        "      Growth Hacker, Digital Marketing Analyst, Campaign Manager,\n"
        "      PPC Specialist, Email Marketing Specialist, Marketing Analyst, Brand Manager\n"
        "- 'QA & Testing Engineer':\n"
        "    - QA Engineer, Test Engineer, SDET, Automation Tester,\n"
        "      Performance Tester, Manual Tester, Quality Analyst,\n"
        "      Test Architect, Regression Tester, Mobile QA Engineer\n"
        "- 'HR & People Ops':\n"
        "    - HR Generalist, HR Business Partner, Talent Acquisition Specialist,\n"
        "      People Operations Manager, Technical Recruiter, HR Coordinator,\n"
        "      Compensation Analyst, HRIS Analyst, Employee Relations Specialist\n"
        "- 'Finance & Accounting':\n"
        "    - Financial Analyst, Accountant, Investment Banking Analyst,\n"
        "      Tax Consultant, Treasury Analyst, Controller, CFO,\n"
        "      Audit Associate, Finance Manager, Payroll Specialist\n"
        "- 'Legal & Compliance':\n"
        "    - Legal Counsel, Compliance Officer, Contract Manager,\n"
        "      Paralegal, Corporate Lawyer, Legal Analyst, Regulatory Affairs Manager\n"
        "- 'Business & Ops':\n"
        "    - Branch Manager, Operations Manager, Supply Chain Analyst,\n"
        "      Administrative Assistant, Procurement Officer, Operations Analyst,\n"
        "      Logistics Coordinator, Inventory Manager, Office Manager\n"
        "- 'Healthcare Professional':\n"
        "    - Doctor, Nurse, Clinical Research Associate, Medical Coder,\n"
        "      Pharmacist, Radiologist, Lab Technician, Medical Officer\n"
        "- 'Education & Training':\n"
        "    - Teacher, Professor, Instructional Designer, Corporate Trainer,\n"
        "      Education Coordinator, Curriculum Developer, Academic Advisor\n"
        "- 'Creative & Content':\n"
        "    - Copywriter, Video Editor, Content Writer, Scriptwriter,\n"
        "      Creative Producer, Content Creator, Editor, Storyboard Artist\n"
        "- 'Sales & Customer Success':\n"
        "    - Account Executive, Customer Success Manager, Business Development Executive,\n"
        "      Sales Development Rep (SDR), Sales Manager, Inside Sales Representative,\n"
        "      Customer Support Specialist, Solutions Consultant\n"
        "- 'Other':\n"
        "    - Entrepreneur, Freelancer, Consultant, Generalist, Unspecified\n\n"
        "- required_skills (list of strings)\n"
        "- required_experience (string):Return just the number of minimum years of experiences required,no range just number, dont mention the job title , just the years\n"
        "- required_education (string or null)\n"
        "- state:Analyse the location specified in the jd and determine the state that is mentioned in the jd,If the value is a city, return its corresponding state . return its corresponding  Standard State name, dont confuse between Delhi or New Delhi etc return a Standard Form with only valid State NAmes.If null, then return Remote(string )\n\n"
        "- country:Analyse the location specified in the jd and determine the country that is mentioned in the jd, if a city is mentioned, find its corresponding country.Based on the given city/country Use Standar country names no abbreviations to avoid any confusion like US or USA UK etc , return United States of America or United Kingdom. If null, then return Remote(string)\n\n"
        "⚠️ Strict Rules:\n"
        "1. Do NOT repeat or duplicate fields.\n"
        "2. Do NOT return extra braces or objects. Output must start and end with a single JSON object.\n"
        "3. All list items (e.g., skills) must be valid strings and comma-separated inside square brackets.\n"
        "4. No extra commentary, explanation, or formatting — just pure valid JSON.\n"
        "5. Use fuzzy matching to handle abbreviation, misspelling, or variations of job titles\n"
        "6. Be inclusive in grouping for `jobtitle_flag`, but dont merge fundamentally different domains\n"
    )
}

def clean_json_text(text):
    """
    Fix common issues in Groq JSON output.
    """
    # ✅ Extract only the JSON part using regex
    json_match = re.search(r"\{[\s\S]*\}", text)
    if json_match:
        cleaned = json_match.group(0)
    else:
        cleaned = text.strip()  # fallback

    # Remove trailing commas
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

    # Remove duplicate fields (basic deduplication)
    seen_fields = set()
    lines = cleaned.splitlines()
    filtered_lines = []
    for line in lines:
        match = re.match(r'"(\w+)"\s*:', line.strip())
        if match:
            key = match.group(1)
            if key in seen_fields:
                continue
            seen_fields.add(key)
        filtered_lines.append(line)
    cleaned = "\n".join(filtered_lines)

    return cleaned

def extract_structured_info_groq_jd(jd_text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            GROQ_SYSTEM_PROMPT_JD,
            {"role": "user", "content": jd_text}
        ],
        "model": GROQ_MODEL,
        "temperature": 0.3,
        "max_tokens": 2048
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        try:
            raw_output = response.json()["choices"][0]["message"]["content"]
            print("🧪 Raw Output from Groq:\n", raw_output)

            # Just extract JSON part
            json_part = re.search(r"\{[\s\S]*\}", raw_output)
            if not json_part:
                print("❌ No JSON found in output.")
                return None

            cleaned = clean_json_text(json_part.group(0))
            return json.loads(cleaned)
        except Exception as e:
            print("❌ JSON Parsing Error:", e)
            return None
    else:
        print("❌ GROQ API Error:", response.status_code, response.text)
        return None


