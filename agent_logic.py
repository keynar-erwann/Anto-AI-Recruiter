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

        # Truncate inputs to avoid token limits
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

        try:
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://incredible-macaron-ec5264.netlify.app",
                    "X-Title": "Anto AI Recruiter",
                },
                model="meta-llama/llama-2-13b-chat:free",  
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an HR analyst. You must analyze the resume and return ONLY a valid JSON object with scores (0-100) and a brief explanation in French. The response must be a properly formatted JSON, nothing else."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1,  # Reduced temperature for more consistent output
                timeout=30  # Increased timeout slightly
            )
            
            # Enhanced response validation
            if not completion or not hasattr(completion, 'choices') or not completion.choices:
                print("AGENT_LOGIC: Invalid API response structure")
                raise ValueError("Invalid API response structure")
                
            response_content = completion.choices[0].message.content.strip()
            print(f"AGENT_LOGIC: Raw API response: {response_content}")
            
            if not response_content:
                raise ValueError("Empty API response")

        except Exception as api_error:
            print(f"AGENT_LOGIC: API call error: {str(api_error)}")
            return {
                "score": 0,
                "skills": 0,
                "experience": 0,
                "education": 0,
                "explanation": f"Erreur lors de l'analyse: {str(api_error)}"
            }

        try:
            # Enhanced JSON cleaning
            cleaned_content = response_content.strip()
            # Remove any markdown code block indicators
            if cleaned_content.startswith('```'):
                cleaned_content = cleaned_content.split('```')[1]
            if cleaned_content.startswith('json'):
                cleaned_content = cleaned_content[4:].strip()
            cleaned_content = cleaned_content.strip('`').strip()
            
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
                missing_fields = [field for field in required_fields if field not in parsed_response]
                print(f"AGENT_LOGIC: Missing fields in response: {missing_fields}")
                return {
                    "score": 0,
                    "skills": 0,
                    "experience": 0,
                    "education": 0,
                    "explanation": "L'analyse a produit une réponse incomplète."
                }
                
        except json.JSONDecodeError as json_error:
            print(f"AGENT_LOGIC: JSON parsing error: {str(json_error)}")
            print(f"AGENT_LOGIC: Failed content: {response_content}")
            return {
                "score": 0,
                "skills": 0,
                "experience": 0,
                "education": 0,
                "explanation": "Le format de la réponse est invalide."
            }

    except Exception as e:
        print(f"AGENT_LOGIC: Analysis error: {str(e)}")
        return {
            "score": 0,
            "skills": 0,
            "experience": 0,
            "education": 0,
            "explanation": f"Erreur lors de l'analyse: {str(e)}"
        }