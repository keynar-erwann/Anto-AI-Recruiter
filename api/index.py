import sys
from mangum import Mangum

# Add parent directory to Python path
sys.path.append('..')

# Import the app
from main import app

# Create handler instance
handler = Mangum(app)