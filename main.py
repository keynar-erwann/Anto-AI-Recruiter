from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

print("MAIN.PY: Starting import...")

try:
    print("MAIN.PY: Attempting to import from agent_logic...")
    from agent_logic import analyze_resume
    print("MAIN.PY: Successfully imported from agent_logic.")
except Exception as e:
    print(f"MAIN.PY: ERROR importing from agent_logic - {e}")
    raise

print("MAIN.PY: Initializing FastAPI app...")
app = FastAPI()
print("MAIN.PY: FastAPI app initialized.")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://incredible-macaron-ec5264.netlify.app",  
    "https://anto-ai-recruiter.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeAnalysisRequest(BaseModel):
    job_description: str
    files: list[dict[str, str]]

@app.get("/")
async def health_check():
    return {"status": "active", "api_version": "1.0"}

@app.post("/analyze")
async def analyze_multiple_resumes_endpoint(request: ResumeAnalysisRequest):
    print("MAIN.PY: /analyze endpoint called.")
    results = []
    errors = []
    try:
        for file_info in request.files:
            filename = file_info.get("name", "Unknown Filename")
            resume_text = file_info.get("content")
            print(f"MAIN.PY: Analyzing file: {filename}")
            
            try:
                if resume_text:
                    analysis_result = analyze_resume(request.job_description, resume_text)
                    if isinstance(analysis_result, dict):
                        if "error" in analysis_result:
                            errors.append({"filename": filename, "error": analysis_result["error"]})
                        else:
                            analysis_result['filename'] = filename
                            results.append(analysis_result)
                    else:
                        errors.append({"filename": filename, "error": "Invalid analysis result format"})
                else:
                    errors.append({"filename": filename, "error": "Missing content for file"})
            except Exception as file_error:
                print(f"MAIN.PY: Error processing {filename}: {str(file_error)}")
                errors.append({"filename": filename, "error": str(file_error)})
                continue

        return {"candidates": results, "errors": errors}

    except Exception as e:
        print(f"MAIN.PY: Unexpected error in /analyze endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={"candidates": [], "errors": [{"filename": "system", "error": str(e)}]}
        )

print("MAIN.PY: Finished import and setup.")