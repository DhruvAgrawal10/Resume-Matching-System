import requests
import json
import re
import time

GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-70b-8192"
# GROQ_MODEL = "llama3-8b-8192"

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a highly accurate AI resume parser with high knowledge of vast range of job titlesa nd industries as well as high geographical knowledge that extracts structured information from unstructured resumes.\n"
        "You must return ONLY a JSON object with the following fields:\n\n"
        "- name (string)\n"
        "- state (string): If the value is a city, return its corresponding  Standard State name, dont confuse between Delhi or New Delhi etc return a Standard Form with only valid State NAmes\n"
        "- country (string): Based on the given city/country Use Standar country names no abbreviations to avoid any confusion like US or USA UK etc , return United States of America or United Kingdom\n"
        "- job_title (string): Extract the most recent or most relevant job title from experience or summary\n"
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
        "- skills (list of strings): Extract from the resume. Prefer skills relevant to the jobtitle_flag\n"
        "- experience (list of objects): Each object should include:\n"
        "    - company (string)\n"
        "    - title (string)\n"
        "    - duration (string): 'YYYY-MM to YYYY-MM'\n"
        "    - description (string)\n"
        "- years_of_relevant_experience (string):\n"
        "    - Return just the number of years of experiences required,no range just number, dont mention the job title , just the years.\n"
        "    - If no relevant experience, return '0'\n"
        "    - Estimate how many years the candidate has worked in job roles that match the inferred `jobtitle_flag`\n"
        "    - Ignore unrelated roles. Only count job titles aligned to the inferred flag.\n"
        "- education (list of objects): Each object should include:\n"
        "    - institution (string)\n"
        "    - degree (string)\n"
        "    - field (string)\n"
        "    - year (string or null)\n\n"
         "- total_yrs_of_exp (string):\n"
        "    - Return just the number of years of total experiences  ,no range just number, dont mention the job title , just the years.\n"
        "    - If no relevant experience, return '0'\n"
        "    - Estimate how many years the candidate has worked in total in any role\n"
        "Rules:\n"
        "1. If any field is missing in the resume, return null or an empty list\n"
        "2. Return clean valid JSON with no extra explanation\n"
        "3. Use fuzzy matching to handle abbreviation, misspelling, or variations of job titles\n"
        "4. Be inclusive in grouping for `jobtitle_flag`, but dont merge fundamentally different domains\n"
        "5. Do not repeat titles from the experience section if they are irrelevant to the final jobtitle_flag\n"
        "6. If the resume has no relevant experience, return '0 years' for `years_of_relevant_experience`\n\n"
        "Example 1:\n"
        "{\n"
        "  \"name\": \"Ankita Verma\",\n"
        "  \"state\": \"Andhra Pradesh\",\n"
        "  \"country\": \"India\",\n"
        "  \"job_title\": \"Java Developer\",\n"
        "  \"jobtitle_flag\": \"Software Developer\",\n"
        "  \"skills\": [\"Java\", \"Spring Boot\", \"Microservices\"],\n"
        "  \"experience\": [\n"
        "    {\n"
        "      \"company\": \"Infosys\",\n"
        "      \"title\": \"Java Developer\",\n"
        "      \"duration\": \"2021-07 to 2023-10\",\n"
        "      \"description\": \"Worked on scalable backend services.\"\n"
        "    },\n"
        "    {\n"
        "      \"company\": \"ABC Designs\",\n"
        "      \"title\": \"UX Designer\",\n"
        "      \"duration\": \"2019-01 to 2021-06\",\n"
        "      \"description\": \"Designed web interfaces.\"\n"
        "    }\n"
        "  ],\n"
        "  \"years_of_relevant_experience\": \"2\",\n"
        "  \"education\": [\n"
        "    {\n"
        "      \"institution\": \"NIT Trichy\",\n"
        "      \"degree\": \"B.Tech\",\n"
        "      \"field\": \"Computer Science\",\n"
        "      \"year\": \"2021\"\n"
        "    }\n"
        "  ]\n"
        "  \"total_yrs_of_exp\": \"4\"\n"
        "}\n"
    )
}


def extract_resume_metadata(text: str, max_retries=5) -> dict:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            SYSTEM_PROMPT,
            {"role": "user", "content": text[:10000]}
        ],
        "temperature": 0.2,
        "max_tokens": 2048
    }

    retries = 0
    while retries < max_retries:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            break
        elif response.status_code == 429:
            try:
                error_json = response.json()
                message = error_json.get("error", {}).get("message", "")
                wait_time = float(re.search(r"try again in ([\d.]+)s", message).group(1))
                print(f"⏳ Rate limit hit. Waiting {wait_time:.2f} seconds before retrying...")
                time.sleep(wait_time + 1)
                retries += 1
                continue
            except Exception:
                print("⚠️ Could not parse retry time. Waiting 10s...")
                time.sleep(10)
                retries += 1
                continue
        else:
            raise Exception(f"❌ GROQ API error {response.status_code}: {response.text}")

    if retries == max_retries:
        raise Exception("❌ Exceeded maximum retry attempts for GROQ API rate limit.")

    try:
        content = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise Exception(f"❌ Failed to extract content from response: {response.text}") from e

    match = re.search(r"\{[\s\S]*\}", content)
    if not match:
        raise ValueError("⚠️ Could not find a valid JSON block in LLM response.")

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        print("⚠️ Warning: Model returned invalid JSON. Raw content:")
        print(match.group())
        raise Exception("❌ Could not parse JSON from LLM output.")
