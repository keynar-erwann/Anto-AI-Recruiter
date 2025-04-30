import os
import json
from openai import OpenAI
from dotenv import load_dotenv

print("AGENT_LOGIC: Starting import...")
load_dotenv()

# Initialize OpenAI client with OpenRouter configuration
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def analyze_resume(job_description: str, resume_text: str) -> dict:
    print("AGENT_LOGIC: analyze_resume function called.")
    try:
        prompt = f"""
        Job Description:
        {job_description}

        Resume:
        {resume_text}

        Please analyze this resume against the job description and provide a JSON object with EXACTLY this structure:
        {{
            "score": <number between 0-100>,
            "skills": <number between 0-100>,
            "experience": <number between 0-100>,
            "education": <number between 0-100>,
            "explanation": <string with analysis details>
        }}

        Return ONLY the JSON object, no additional text.
        """

        # Make API call with the new format
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://incredible-macaron-ec5264.netlify.app",
                "X-Title": "Anto AI Recruiter",
            },
            model="deepseek/deepseek-r1-zero:free",
            messages=[
                {"role": "system", "content": "You are a professional HR analyst. You must return only valid JSON matching the exact structure requested."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        # Parse the response content as JSON
        response_content = completion.choices[0].message.content.strip()
        try:
            parsed_response = json.loads(response_content)
            
            # Vérifier que la réponse a la structure attendue
            required_fields = ["score", "skills", "experience", "education", "explanation"]
            if all(field in parsed_response for field in required_fields):
                return parsed_response
            else:
                print("AGENT_LOGIC: Réponse JSON invalide - champs manquants")
                return {"error": "Format de réponse invalide - champs manquants"}
                
        except json.JSONDecodeError as json_error:
            print(f"AGENT_LOGIC: Erreur de parsing JSON: {str(json_error)}")
            return {"error": "Format de réponse invalide"}

    except Exception as e:
        print(f"AGENT_LOGIC: Error during analysis: {str(e)}")
        return {"error": f"Erreur d'analyse: {str(e)}"}