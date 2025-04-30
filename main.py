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
            if resume_text:
                # Truncate resume_text to approximately 2000 tokens (about 8000 characters)
                truncated_text = resume_text[:8000] if len(resume_text) > 8000 else resume_text
                try:
                    analysis_result = analyze_resume(request.job_description, truncated_text)
                    if analysis_result:
                        analysis_result['filename'] = filename
                        if len(resume_text) > 8000:
                            analysis_result['warning'] = "CV was truncated due to length limitations"
                        results.append(analysis_result)
                    else:
                        print(f"MAIN.PY: Analysis returned None for {filename}")
                        errors.append({"filename": filename, "error": "Analysis failed or returned no result"})
                except Exception as analysis_error:
                    print(f"MAIN.PY: Error analyzing {filename}: {str(analysis_error)}")
                    errors.append({"filename": filename, "error": str(analysis_error)})
            else:
                errors.append({"filename": filename, "error": "Missing content for file"})

        return {"candidates": results, "errors": errors}

    except Exception as e:
        print(f"MAIN.PY: Unexpected error in /analyze endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")