import sys
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


sys.path.append('..')

try:
    
    from main import app
    logger.info("Successfully imported FastAPI app")
except Exception as e:
    logger.error(f"Failed to import FastAPI app: {str(e)}")
    raise
