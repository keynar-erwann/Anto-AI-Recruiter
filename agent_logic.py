import os
import json
from groq import Groq
from dotenv import load_dotenv

print("AGENT_LOGIC: Starting import...") # ADDED
load_dotenv()

print("AGENT_LOGIC: Attempting to get GROQ_API_KEY...") # ADDED
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("AGENT_LOGIC: ERROR - GROQ_API_KEY not found!") # ADDED
    # Optionally raise an error here if you want it to fail explicitly
    # raise ValueError("GROQ_API_KEY environment variable not set.")
else:
    print("AGENT_LOGIC: GROQ_API_KEY found. Initializing Groq client...") # ADDED

# Wrap the client initialization in a try-except block for more detailed error logging
try:
    groq_client = Groq(
        api_key=api_key
    )
    print("AGENT_LOGIC: Groq client initialized successfully.") # ADDED
except Exception as e:
    print(f"AGENT_LOGIC: ERROR initializing Groq client - {e}") # ADDED
    raise # Re-raise the exception to ensure the failure is logged

def extract_json_from_string(string):
    """Safely extract JSON object from a messy string."""
    if isinstance(string, str) and string.strip().startswith("FINAL_JSON:"):
        string = string.strip()[len("FINAL_JSON:"):].strip()

    try:
        start = string.find('{')
        end = string.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = string[start:end]
            return json.loads(json_str)
        else:
            print(f"Warning: Could not find valid JSON structure in string: {string}")
            return None
    except json.JSONDecodeError as e:
        problematic_json_str = string[start:end] if start != -1 and end != 0 else string
        print(f"JSON decoding error: {e} in string segment: {problematic_json_str}")
        return None
    except Exception as e:
        print(f"Unexpected JSON extraction error: {e}")
        return None

def analyze_resume(job_description, resume_text):
    """Analyze a single resume against the job description."""
    print("AGENT_LOGIC: analyze_resume function called.") # ADDED

    prompt = f"""
Tu es Anto, un recruteur IA expert. À partir de la description de poste et du CV ci-dessous :

- Analyse et donne-moi uniquement ce JSON au format suivant :
{{
  "overall_score": <0-100>,
  "skills_match": <0-100>,
  "experience_match": <0-100>,
  "education_match": <0-100>,
  "short_explanation": "explication naturelle en français sur la pertinence ou non du candidat en quelques phrases"
}}

Aucune explication supplémentaire, juste le JSON valide.

---

Description du poste:
{job_description}

CV:
{resume_text}
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=800,
        )

        raw_content = response.choices[0].message.content.strip()
        parsed = extract_json_from_string(raw_content)

        return parsed

    except Exception as e:
        print(f"Erreur d'analyse: {e}")
        return None

print("AGENT_LOGIC: Finished import.") # ADDED