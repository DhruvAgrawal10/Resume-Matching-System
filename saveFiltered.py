import json
import os
import re
from datetime import datetime

def slugify_filename(text):
    return re.sub(r'[^a-z0-9_]+', '_', text.lower()).strip('_')

def make_json_serializable(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # e.g., "2025-07-15T05:20:20"
    if isinstance(obj, list):
        return [make_json_serializable(i) for i in obj]
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    return obj

def save_matches_to_json(matches, output_dir=r"C:\Users\User\.vscode\PYTHON PRACTICE\InfoOrigin-Internship\ResumeMatching\results", jd_info=None):
    if not matches:
        print("⚠️ No matches to save.")
        return None

    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    jd_title = jd_info.get("jobtitle_flag") or jd_info.get("job_title", "unknown")
    jd_title_slug = slugify_filename(jd_title)
    filename = f"{jd_title_slug}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    # ✅ Convert all datetime fields to strings
    safe_matches = make_json_serializable(matches)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(safe_matches, f, indent=2, ensure_ascii=False)

    print(f"\n📦 Results saved to {filepath}")
    return filepath