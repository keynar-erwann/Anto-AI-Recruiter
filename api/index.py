from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

import sys
sys.path.append('..')  # Allow imports from parent directory

from main import app as fastapi_app  # Assuming your FastAPI app is called 'app' in main.py

# Add CORS (important for frontend connection)
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(fastapi_app)
