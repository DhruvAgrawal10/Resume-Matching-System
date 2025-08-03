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
        "You are an AI resume parser that extracts structured information.\n\n"
        "Return ONLY a JSON object with the following fields:\n"
        "- name (string)\n"
        "- state (string): If the fetched entity or string is a city name, then find and return its corresponding state\n"
        "- country (string)\n"
        "- job_title (string)\n"
        "- jobtitle_flag (string): This is the canonical job domain label inferred from resume content.\n"
        "   Group similar job titles like:\n"
        "   - 'Python Developer', 'Java Developer', 'Software Engineer', 'Backend Developer' → 'Software Developer'\n"
        "   - 'Data Scientist', 'ML Engineer', 'Data Engineer', 'Data Science Engineer' → 'Data Scientist'\n"
        "   - 'Frontend Developer', 'React Developer', 'UI Developer' → 'Frontend Developer'\n"
        "   Do NOT group these:\n"
        "   - 'Web Developer' ≠ 'Database Developer' ≠ 'DevOps Engineer' ≠ 'QA Engineer'\n"
        "- skills (list of strings)\n"
        "- experience (list of objects with: company, title, duration, description)\n"
        "- years_of_relevant_experience (string): Estimate how many years the person has worked in job roles matching the inferred jobtitle_flag. \n"
        "   Ignore unrelated roles (e.g., Designer, QA Engineer) even if present in the resume.\n"
        "   Use job titles and context in the experience section to decide what counts as relevant.\n"
        "- education (list of objects with: institution, degree, field, year)\n\n"
        "Rules:\n"
        "1. If any field is missing in the resume, return null or empty array.\n"
        "2. No extra commentary. Return clean valid JSON.\n\n"
        "📘 Examples:\n\n"
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
        "  \"years_of_relevant_experience\": \"2+ years\",\n"
        "  \"education\": [\n"
        "    {\n"
        "      \"institution\": \"NIT Trichy\",\n"
        "      \"degree\": \"B.Tech\",\n"
        "      \"field\": \"Computer Science\",\n"
        "      \"year\": \"2021\"\n"
        "    }\n"
        "  ]\n"
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
