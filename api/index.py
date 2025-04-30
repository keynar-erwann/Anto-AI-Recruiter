import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to Python path
sys.path.append('..')

try:
    # Import the app
    from main import app
    logger.info("Successfully imported FastAPI app")
except Exception as e:
    logger.error(f"Failed to import FastAPI app: {str(e)}")
    raise
