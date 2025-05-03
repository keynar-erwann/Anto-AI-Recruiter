import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import time
import logging

print("AGENT_LOGIC: Starting import...")
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent_logic")

# Verify API key is loaded
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    logger.error("OPENROUTER_API_KEY not found in environment variables")
    raise ValueError("Missing API key - please check your .env file")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def analyze_resume(job_description: str, resume_text: str) -> dict:
    logger.info("AGENT_LOGIC: analyze_resume function called.")
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

        logger.info(f"AGENT_LOGIC: Sending prompt to API (length: {len(prompt)})")

        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                # Log API request details for debugging
                logger.info(f"AGENT_LOGIC: Attempt {attempt+1}/{max_retries} - Calling OpenRouter API")
                
                # Try a different model or adjust parameters
                completion = client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "https://incredible-macaron-ec5264.netlify.app",
                        "X-Title": "Anto AI Recruiter",
                        
                    },
                    
                    model="anthropic/claude-3.5-sonnet",  
                    messages=[
                        {"role": "system", "content": "You are an HR analyst. Return only a valid JSON object with scores and explanation in French."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.2,
                    timeout=30
                )

                
                logger.info(f"AGENT_LOGIC: Received response type: {type(completion)}")
                
               
                response_dict = {}
                for attr in dir(completion):
                    if not attr.startswith('_') and not callable(getattr(completion, attr)):
                        try:
                            response_dict[attr] = getattr(completion, attr)
                        except Exception as e:
                            response_dict[attr] = f"Error accessing: {str(e)}"
                
                logger.info(f"AGENT_LOGIC: Response attributes: {json.dumps(response_dict, default=str)[:500]}...")
                
                if not hasattr(completion, 'choices') or not completion.choices:
                    logger.error(f"AGENT_LOGIC: No choices in response")
                    raise ValueError("No choices in API response")
                
                response_content = completion.choices[0].message.content.strip()
                if not response_content:
                    raise ValueError("Empty content in API response choice.")

                # If we get here, we have a valid response
                logger.info("AGENT_LOGIC: Successfully received valid API response")
                logger.info(f"AGENT_LOGIC: Response content: {response_content[:100]}...")
                break

            except Exception as api_error:
                logger.error(f"AGENT_LOGIC: API call failed: {str(api_error)}")
                if attempt < max_retries - 1:
                    logger.warning(f"AGENT_LOGIC: Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                logger.error(f"AGENT_LOGIC: All API call attempts failed. Final error: {str(api_error)}")
                return {
                    "score": 0,
                    "skills": 0,
                    "experience": 0,
                    "education": 0,
                    "explanation": f"Erreur lors de l'appel API après plusieurs tentatives: {str(api_error)}"
                }

        try:
            cleaned_content = response_content.strip().strip('`').strip()
            if cleaned_content.startswith('```json'):
                cleaned_content = cleaned_content.split('```')[1].strip()
            elif cleaned_content.startswith('```'):
                cleaned_content = cleaned_content.split('```')[1].strip()
            elif cleaned_content.startswith('json'):
                cleaned_content = cleaned_content[4:].strip()

            logger.info(f"AGENT_LOGIC: Cleaned content for parsing: {cleaned_content[:100]}...")
            parsed_response = json.loads(cleaned_content)

            required_fields = ["score", "skills", "experience", "education", "explanation"]
            if all(field in parsed_response for field in required_fields):
                for field in ["score", "skills", "experience", "education"]:
                    try:
                        parsed_response[field] = max(0, min(100, int(float(parsed_response[field]))))
                    except (ValueError, TypeError):
                        parsed_response[field] = 0
                logger.info("AGENT_LOGIC: Successfully parsed and validated response")
                return parsed_response
            else:
                missing = [f for f in required_fields if f not in parsed_response]
                logger.error(f"AGENT_LOGIC: Invalid JSON structure - missing fields: {missing}")
                return {
                    "score": 0,
                    "skills": 0,
                    "experience": 0,
                    "education": 0,
                    "explanation": "L'analyse a produit un format de réponse invalide."
                }

        except json.JSONDecodeError as json_error:
            logger.error(f"AGENT_LOGIC: JSON parsing error: {str(json_error)}")
            logger.error(f"AGENT_LOGIC: Failed content: {response_content}")
            return {
                "score": 0,
                "skills": 0,
                "experience": 0,
                "education": 0,
                "explanation": "Impossible d'analyser les résultats de l'évaluation."
            }

    except Exception as e:
        logger.error(f"AGENT_LOGIC: Analysis error: {str(e)}", exc_info=True)
        return {
            "score": 0,
            "skills": 0,
            "experience": 0,
            "education": 0,
            "explanation": f"Erreur lors de l'analyse : {str(e)}"
        }