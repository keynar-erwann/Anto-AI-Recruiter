print("API/INDEX.PY: Top level execution start.") # ADDED

from fastapi import FastAPI
# Remove duplicate CORS middleware import if not used elsewhere in this file
# from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

import sys
print("API/INDEX.PY: Appending parent directory to sys.path...") # ADDED
sys.path.append('..')  # Allow imports from parent directory
print(f"API/INDEX.PY: sys.path after append: {sys.path}") # ADDED

# Add try-except for main import
try:
    print("API/INDEX.PY: Attempting to import app from main...") # ADDED
    from main import app as fastapi_app  # Assuming your FastAPI app is called 'app' in main.py
    print("API/INDEX.PY: Successfully imported app from main.") # ADDED
except ImportError as e:
    print(f"API/INDEX.PY: ERROR importing from main - {e}") # ADDED
    # If the import fails, we can't proceed. Raise it to make Vercel aware.
    raise
except Exception as e:
    print(f"API/INDEX.PY: UNEXPECTED ERROR during import from main - {e}") # ADDED
    raise


# REMOVED duplicate CORS middleware addition
# fastapi_app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

print("API/INDEX.PY: Initializing Mangum handler...") # ADDED
handler = Mangum(fastapi_app)
print("API/INDEX.PY: Mangum handler initialized.") # ADDED