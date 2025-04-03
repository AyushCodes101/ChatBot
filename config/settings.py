import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""

    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")  # Default to GPT-4

    # File Paths
    SCRAPED_DATA_PATH = "app/data/scraped_data.json"
    FAISS_INDEX_PATH = "app/faiss_index/index.faiss"
    LOG_FILE_PATH = "app/logs/app.log"

    # FAISS Indexing Configuration
    EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's embedding model
    CHUNK_SIZE = 500  # Adjust chunk size as per your needs

    # Scraper Configuration
    MAX_RETRIES = 3  # Number of retries if a request fails
    TIMEOUT = 10  # Timeout for requests in seconds
    FOLLOW_INTERNAL_LINKS = True  # Set to False to disable following subpages

# Initialize settings
settings = Settings()
