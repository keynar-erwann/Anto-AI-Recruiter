from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import asyncio

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

# ... existing code ...

@app.post("/analyze")
async def analyze_multiple_resumes_endpoint(request: ResumeAnalysisRequest):
    print("MAIN.PY: /analyze endpoint called.")
    results = []
    errors = []
    try:
        # Process files concurrently with a timeout
        async def process_file(file_info):
            try:
                filename = file_info.get("name", "Unknown Filename")
                resume_text = file_info.get("content")
                print(f"MAIN.PY: Analyzing file: {filename}")
                
                if resume_text:
                    # Set a timeout for each file analysis
                    try:
                        analysis_result = await asyncio.wait_for(
                            asyncio.to_thread(analyze_resume, request.job_description, resume_text),
                            timeout=45  # 45 seconds timeout per file
                        )
                        if isinstance(analysis_result, dict):
                            if "error" in analysis_result:
                                return {"error": True, "filename": filename, "message": analysis_result["error"]}
                            else:
                                analysis_result['filename'] = filename
                                return {"error": False, "result": analysis_result}
                        else:
                            return {"error": True, "filename": filename, "message": "Invalid analysis result format"}
                    except asyncio.TimeoutError:
                        return {"error": True, "filename": filename, "message": "Analysis timed out"}
                else:
                    return {"error": True, "filename": filename, "message": "Missing content for file"}
            except Exception as e:
                return {"error": True, "filename": filename, "message": str(e)}

        # Process all files concurrently
        tasks = [process_file(file_info) for file_info in request.files]
        file_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect results and errors
        for result in file_results:
            if isinstance(result, dict):
                if result.get("error"):
                    errors.append({"filename": result["filename"], "error": result["message"]})
                else:
                    results.append(result["result"])
            else:
                errors.append({"filename": "unknown", "error": str(result)})

        return {"candidates": results, "errors": errors}

    except Exception as e:
        print(f"MAIN.PY: Unexpected error in /analyze endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={"candidates": [], "errors": [{"filename": "system", "error": str(e)}]}
        )