print("API/INDEX.PY: Top level execution start (Minimal Test).")

from fastapi import FastAPI
from mangum import Mangum
from fastapi.responses import JSONResponse

# Create a minimal FastAPI app directly in this file
minimal_app = FastAPI()

# Define a simple test route at /api/test
@minimal_app.get("/api/test")
async def read_root():
    print("API/INDEX.PY: Minimal /api/test endpoint called.")
    return JSONResponse(content={"message": "Minimal API is working!"})

# Wrap the minimal app with Mangum
print("API/INDEX.PY: Initializing Mangum handler for minimal app...")
handler = Mangum(minimal_app)
print("API/INDEX.PY: Mangum handler initialized for minimal app.")

# --- Code below is commented out for this test ---
# import sys
# print("API/INDEX.PY: Appending parent directory to sys.path...")
# sys.path.append('..')
# print(f"API/INDEX.PY: sys.path after append: {sys.path}")
#
# try:
#     print("API/INDEX.PY: Attempting to import app from main...")
#     # Import 'app' directly without aliasing
#     from main import app
#     print("API/INDEX.PY: Successfully imported app from main.")
# except ImportError as e:
#     print(f"API/INDEX.PY: ERROR importing from main - {e}")
#     raise
# except Exception as e:
#     print(f"API/INDEX.PY: UNEXPECTED ERROR during import from main - {e}")
#     raise
#
# # Initialize Mangum with the imported 'app'
# print("API/INDEX.PY: Initializing Mangum handler...")
# handler = Mangum(app)
# print("API/INDEX.PY: Mangum handler initialized.")