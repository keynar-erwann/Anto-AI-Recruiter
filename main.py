from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_logic import analyze_resume

app = FastAPI()


class ResumeAnalysisRequest(BaseModel):
    job_description: str
    resume_text: str

@app.post("/analyze")
async def analyze_resume_endpoint(request: ResumeAnalysisRequest):
    try:
        result = analyze_resume(request.job_description, request.resume_text)
        if result is None:
            raise HTTPException(status_code=400, detail="Analysis failed")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from mangum import Mangum
handler = Mangum(app)
