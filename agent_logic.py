import os
import json
from openai import OpenAI
from dotenv import load_dotenv

print("AGENT_LOGIC: Starting import...")
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def analyze_resume(job_description: str, resume_text: str) -> dict:
    print("AGENT_LOGIC: analyze_resume function called.")
    try:
       
        if not resume_text or len(resume_text.strip()) < 50:
            return {
                "score": 0,
                "skills": 0,
                "experience": 0,
                "education": 0,
                "explanation": "Le CV semble être vide ou contient un contenu insuffisant pour l'analyse."
            }

       
        max_length = 1500
        truncated_resume = resume_text[:max_length] if len(resume_text) > max_length else resume_text
        truncated_job = job_description[:max_length] if len(job_description) > max_length else job_description

        prompt = f"""
        Analyze this resume against the job requirements and return ONLY a JSON object with exactly this structure:
        {{
            "score": <0-100>,
            "skills": <0-100>,
            "experience": <0-100>,
            "education": <0-100>,
            "explanation": <brief analysis in French>
        }}

        Job Description: {truncated_job}
        Resume: {truncated_resume}
        """

        
        print(f"AGENT_LOGIC: Sending prompt to API:\n{prompt}\n--- End of Prompt ---")

        try:
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://incredible-macaron-ec5264.netlify.app",
                    "X-Title": "Anto AI Recruiter",
                },
                model="google/gemini-flash-1.5-8b-exp",
                messages=[
                    {"role": "system", "content": "You are an HR analyst. Return only a valid JSON object with scores and explanation in French."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.2,
                timeout=25
            )

            
            if not completion:
                print("AGENT_LOGIC: Empty API response object received.")
                raise ValueError("Empty API response object received.")

           
            if not hasattr(completion, 'choices') or not completion.choices:
                print(f"AGENT_LOGIC: No choices in API response. Full response object: {completion}") 
                raise ValueError("No choices in API response")

            response_content = completion.choices[0].message.content.strip()
            print(f"AGENT_LOGIC: Raw API response content: {response_content}")

            
            if not response_content:
                print("AGENT_LOGIC: Empty content in API response choice.")
                raise ValueError("Empty content in API response choice.")

        except Exception as api_error:
            print(f"AGENT_LOGIC: API call error: {str(api_error)}")
            return {
                "score": 0,
                "skills": 0,
                "experience": 0,
                "education": 0,
                "explanation": f"Erreur lors de l'appel API: {str(api_error)}"
            }

        try:
            
            cleaned_content = response_content.strip().strip('`').strip()
            if cleaned_content.startswith('```json'):
                cleaned_content = cleaned_content.split('```')[1].strip()
            elif cleaned_content.startswith('```'):
                cleaned_content = cleaned_content.split('```')[1].strip()
            elif cleaned_content.startswith('json'):
                cleaned_content = cleaned_content[4:].strip()

            parsed_response = json.loads(cleaned_content)

            required_fields = ["score", "skills", "experience", "education", "explanation"]
            if all(field in parsed_response for field in required_fields):
                for field in ["score", "skills", "experience", "education"]:
                    try:
                        parsed_response[field] = max(0, min(100, int(float(parsed_response[field]))))
                    except (ValueError, TypeError):
                        parsed_response[field] = 0
                return parsed_response
            else:
                print("AGENT_LOGIC: Invalid JSON structure - missing required fields")
                return {
                    "score": 0,
                    "skills": 0,
                    "experience": 0,
                    "education": 0,
                    "explanation": "L'analyse a produit un format de réponse invalide."
                }

        except json.JSONDecodeError as json_error:
            print(f"AGENT_LOGIC: JSON parsing error: {str(json_error)}")
            print(f"AGENT_LOGIC: Failed content: {response_content}")
            return {
                "score": 0,
                "skills": 0,
                "experience": 0,
                "education": 0,
                "explanation": "Impossible d'analyser les résultats de l'évaluation."
            }

    except Exception as e:
        print(f"AGENT_LOGIC: Analysis error: {str(e)}")
        return {
            "score": 0,
            "skills": 0,
            "experience": 0,
            "education": 0,
            "explanation": f"Erreur lors de l'analyse : {str(e)}"
        }