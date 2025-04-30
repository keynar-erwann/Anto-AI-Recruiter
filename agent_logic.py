import os
from openrouter import OpenRouter
from dotenv import load_dotenv


load_dotenv()

# Initialize OpenRouter client
client = OpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="deepseek/deepseek-r1-zero:free"  
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

        # Make API call
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional HR analyst specializing in resume evaluation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        
        return response.choices[0].message.content

    except Exception as e:
        print(f"Erreur d'analyse: {str(e)}")
        return None