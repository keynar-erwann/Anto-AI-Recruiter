from pydantic import BaseModel, Field
from typing import List, Optional

class Candidate(BaseModel):
    filename: str
    score: float = Field(ge=0, le=100)
    skills: float = Field(ge=0, le=100)
    experience: float = Field(ge=0, le=100)
    education: float = Field(ge=0, le=100)
    explanation: str
    error: Optional[str] = None

class AnalysisRequest(BaseModel):
    job_description: str
    files: List[str]  # List of file paths or base64 encoded files

class AnalysisResponse(BaseModel):
    candidates: List[Candidate]
    errors: List[Candidate] = []