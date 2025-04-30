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

        Please analyze this resume against the job description and provide:
        1. Overall match score (0-100)
        2. Key skills that match the job requirements
        3. Missing skills or gaps
        4. Years of relevant experience
        5. Educational background relevance
        6. Recommendations for the candidate

        Format the response as a JSON object.
        """

        # Make API call with the new format
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://incredible-macaron-ec5264.netlify.app",
                "X-Title": "Anto AI Recruiter",
            },
            model="deepseek/deepseek-r1-zero:free",
            messages=[
                {"role": "system", "content": "You are a professional HR analyst specializing in resume evaluation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        # Parse the response content as JSON
        response_content = completion.choices[0].message.content
        try:
            # Tenter de parser la réponse en JSON
            parsed_response = json.loads(response_content)
            return parsed_response  # Retourner l'objet JSON parsé
        except json.JSONDecodeError as json_error:
            print(f"AGENT_LOGIC: Erreur de parsing JSON: {str(json_error)}")
            return {"error": "Format de réponse invalide"}

    except Exception as e:
        print(f"AGENT_LOGIC: Error during analysis: {str(e)}")
        return {"error": f"Erreur d'analyse: {str(e)}"}