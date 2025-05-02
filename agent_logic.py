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

        Analyze this resume against the job description and return ONLY a JSON object with this EXACT structure, no other text:
        {{
            "score": <integer 0-100>,
            "skills": <integer 0-100>,
            "experience": <integer 0-100>,
            "education": <integer 0-100>,
            "explanation": <brief analysis>
        }}
        """

        # Make API call with the new format
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://incredible-macaron-ec5264.netlify.app",
                "X-Title": "Anto AI Recruiter",
            },
            model="deepseek/deepseek-r1-zero:free",
            messages=[
                {"role": "system", "content": "You are a professional HR analyst. You must return only a valid JSON object with the exact structure requested, no additional text or formatting."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3,
            timeout=30
        )

        # Parse the response content as JSON
        response_content = completion.choices[0].message.content.strip()
        print(f"AGENT_LOGIC: Raw API response: {response_content}")
        
        try:
            parsed_response = json.loads(response_content)
            
            # Validate response structure
            required_fields = ["score", "skills", "experience", "education", "explanation"]
            if all(field in parsed_response for field in required_fields):
                # Ensure all numeric fields are integers between 0-100
                for field in ["score", "skills", "experience", "education"]:
                    parsed_response[field] = max(0, min(100, int(parsed_response[field])))
                return parsed_response
            else:
                print("AGENT_LOGIC: Invalid JSON structure - missing required fields")
                return {"error": "Invalid response format - missing required fields"}
                
        except json.JSONDecodeError as json_error:
            print(f"AGENT_LOGIC: JSON parsing error: {str(json_error)}")
            print(f"AGENT_LOGIC: Failed content: {response_content}")
            return {"error": "Invalid response format"}

    except Exception as e:
        print(f"AGENT_LOGIC: Analysis error: {str(e)}")
        return {"error": f"Analysis failed: {str(e)}"}