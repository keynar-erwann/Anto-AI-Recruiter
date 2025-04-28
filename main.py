from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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


class ResumeAnalysisRequest(BaseModel):
    job_description: str
    resume_text: str

@app.post("/analyze")
async def analyze_resume_endpoint(request: ResumeAnalysisRequest):
    print("MAIN.PY: /analyze endpoint called.") # ADDED
    try:
        result = analyze_resume(request.job_description, request.resume_text)
        if result is None:
            # Adding a print here too for debugging failed analysis
            print("MAIN.PY: Analysis returned None, raising HTTPException 400.") # ADDED
            raise HTTPException(status_code=400, detail="Analysis failed or returned no result")
        return result
    except HTTPException as http_exc:
        # Re-raise HTTPExceptions directly
        raise http_exc
    except Exception as e:
        # Log other exceptions before raising HTTPException 500
        print(f"MAIN.PY: Unexpected error in /analyze endpoint: {e}") # ADDED
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


# This part should ideally be in api/index.py for Vercel,
# but if you are running locally or need it here for some reason:
# from mangum import Mangum
# handler = Mangum(app)

print("MAIN.PY: Finished import and setup.") # ADDED