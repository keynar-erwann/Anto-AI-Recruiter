from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware
import os # Import os to potentially get allowed origins from env vars

print("MAIN.PY: Starting import...") # ADDED

# Add a try-except block around the import that might fail
try:
    print("MAIN.PY: Attempting to import from agent_logic...") # ADDED
    from agent_logic import analyze_resume
    print("MAIN.PY: Successfully imported from agent_logic.") # ADDED
except Exception as e:
    print(f"MAIN.PY: ERROR importing from agent_logic - {e}") # ADDED
    raise # Re-raise to ensure failure

print("MAIN.PY: Initializing FastAPI app...") # ADDED
app = FastAPI()
print("MAIN.PY: FastAPI app initialized.") # ADDED

# --- Add CORS Middleware ---
# Define the origins allowed to access your backend.
# IMPORTANT: Replace "https://your-netlify-site-name.netlify.app" with your actual Netlify frontend URL.
# You can also use ["*"] to allow all origins during development, but be more specific for production.
# Consider using an environment variable for the frontend URL in production.
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "incredible-macaron-ec5264.netlify.app",  
    "https://anto-ai-recruiter.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)
# --- End CORS Middleware ---


class ResumeAnalysisRequest(BaseModel):
    job_description: str
    # Ensure this matches the structure sent by the frontend
    # If frontend sends {name: string, content: string}[]
    files: list[dict[str, str]]
    # If frontend sends {job_description: string, resume_text: string} (like original main.py)
    # resume_text: str # Uncomment this if using single resume analysis endpoint

@app.get("/")
async def health_check():
    return {"status": "active", "api_version": "1.0"}
@app.post("/analyze")
# async def analyze_resume_endpoint(request: ResumeAnalysisRequest): # Use this if expecting ONE resume_text
async def analyze_multiple_resumes_endpoint(request: ResumeAnalysisRequest): # Use this if expecting list of files
    print("MAIN.PY: /analyze endpoint called.") # ADDED
    results = []
    errors = []
    try:
        # Loop through files sent from the frontend
        for file_info in request.files:
            filename = file_info.get("name", "Unknown Filename")
            resume_text = file_info.get("content")
            print(f"MAIN.PY: Analyzing file: {filename}") # ADDED
            if resume_text:
                analysis_result = analyze_resume(request.job_description, resume_text)
                if analysis_result:
                    # Add filename to the result before sending back
                    analysis_result['filename'] = filename
                    results.append(analysis_result)
                else:
                    print(f"MAIN.PY: Analysis returned None for {filename}") # ADDED
                    errors.append({"filename": filename, "error": "Analysis failed or returned no result"})
            else:
                 errors.append({"filename": filename, "error": "Missing content for file"})

        # Return the structure expected by the frontend { candidates: [], errors: [] }
        return {"candidates": results, "errors": errors}

    except Exception as e:
        # Log other exceptions before raising HTTPException 500
        print(f"MAIN.PY: Unexpected error in /analyze endpoint: {e}") # ADDED
        # You might want to return a structured error instead of raising 500 for partial failures
        # For now, let's keep the 500 for general errors during processing
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
# --- End Endpoint Adjustment ---


# This part should ideally be in api/index.py for Vercel,
# but if you are running locally or need it here for some reason:

print("MAIN.PY: Finished import and setup.") # ADDED