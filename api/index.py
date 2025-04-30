print("API/INDEX.PY: Top level execution start.")

from mangum import Mangum
import sys

print("API/INDEX.PY: Appending parent directory to sys.path...")
sys.path.append('..')
print(f"API/INDEX.PY: sys.path after append: {sys.path}")

try:
    print("API/INDEX.PY: Attempting to import app from main...")
    # Import 'app' directly without aliasing
    from main import app
    print("API/INDEX.PY: Successfully imported app from main.")
except ImportError as e:
    print(f"API/INDEX.PY: ERROR importing from main - {e}")
    raise

# Initialize Mangum with the correct handler format
print("API/INDEX.PY: Initializing Mangum handler...")
handler = Mangum(app, lifespan="off")  # Add lifespan parameter
print("API/INDEX.PY: Mangum handler initialized.")