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
        # Truncate inputs to avoid token limits
        max_length = 1500
        truncated_resume = resume_text[:max_length] if len(resume_text) > max_length else resume_text
        truncated_job = job_description[:max_length] if len(job_description) > max_length else job_description

        prompt = f"""
        Analyze this resume against the job requirements. Return a JSON object with this structure:
        {{
            "score": <0-100>,
            "skills": <0-100>,
            "experience": <0-100>,
            "education": <0-100>,
            "explanation": <brief analysis>
        }}

        Job Description: {truncated_job}
        Resume: {truncated_resume}

        Return ONLY the JSON object, no other text.
        """

        # Make API call with optimized parameters for Gemma
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://incredible-macaron-ec5264.netlify.app",
                "X-Title": "Anto AI Recruiter",
            },
            model="gemma-3-27b-it:free",
            messages=[
                {"role": "system", "content": "You are an HR analyst. Return only valid JSON matching the exact structure requested."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # Reduced tokens for faster response
            temperature=0.2,  # Lower temperature for more consistent output
            timeout=25  # Shorter timeout
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
                    try:
                        parsed_response[field] = max(0, min(100, int(float(parsed_response[field]))))
                    except (ValueError, TypeError):
                        parsed_response[field] = 0
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