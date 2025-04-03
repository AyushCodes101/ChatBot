import logging
import os
from datetime import datetime
from app.config.settings import settings

# Ensure the logs directory exists
os.makedirs("app/logs", exist_ok=True)

# Define log file path
LOG_FILE = settings.LOG_FILE_PATH

# Custom log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default logging level
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8'),
        logging.StreamHandler()  # Prints logs to console
    ]
)

# Create logger
logger = logging.getLogger("RAG_Chatbot")

# Add a startup log entry
logger.info(f"🚀 Logger initialized at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
