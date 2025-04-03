import os
import json
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.config.logger import logger
from app.config.settings import settings

class VectorStore:
    """Handles text embedding and FAISS vector storage."""

    def __init__(self):
        self.faiss_index_path = settings.FAISS_INDEX_PATH
        self.scraped_data_path = settings.SCRAPED_DATA_PATH

        # Ensure FAISS index directory exists
        os.makedirs(self.faiss_index_path, exist_ok=True)

        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None

    def load_scraped_data(self):
        """Loads the scraped data from JSON."""
        if not os.path.exists(self.scraped_data_path):
            logger.error("Scraped data not found. Run the scraper first.")
            return []

        try:
            with open(self.scraped_data_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            logger.info("Loaded scraped data successfully.")
            return data
        except json.JSONDecodeError:
            logger.error("Failed to load scraped data. JSON file may be corrupted.")
            return []

    def create_index(self):
        """Processes scraped data and creates a FAISS index."""
        data = self.load_scraped_data()
        if not data:
            logger.error("No data to index. Exiting...")
            return

        logger.info("Processing data for FAISS index...")
        documents = [entry["content"] for entry in data if "content" in entry]

        # Use SemanticChunker for better context-aware chunking
        text_splitter = SemanticChunker(self.embeddings)
        chunks = []
        for doc in documents:
            chunks.extend(text_splitter.split_text(doc))

        if not chunks:
            logger.error("No valid text chunks found for indexing.")
            return

        try:
            self.vector_store = FAISS.from_texts(chunks, self.embeddings)
            self.vector_store.save_local(self.faiss_index_path)
            logger.info("FAISS index created and saved successfully.")
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")

    def load_index(self):
        """Loads the FAISS index if it exists, otherwise creates a new one."""
        if os.path.exists(os.path.join(self.faiss_index_path, "index.faiss")):
            try:
                self.vector_store = FAISS.load_local(self.faiss_index_path, self.embeddings)
                logger.info("FAISS index loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading FAISS index: {e}")
                logger.info("Attempting to create a new FAISS index...")
                self.create_index()
        else:
            logger.info("FAISS index not found. Creating a new one...")
            self.create_index()

    def search(self, query, k=5):
        """Searches the FAISS index for relevant results."""
        if not self.vector_store:
            logger.error("FAISS index not loaded. Exiting...")
            return []

        try:
            results = self.vector_store.similarity_search(query, k=k)
            return [result.page_content for result in results]
        except Exception as e:
            logger.error(f"Error searching FAISS index: {e}")
            return []

# If running this file directly, test indexing
if __name__ == "__main__":
    vector_store = VectorStore()
    vector_store.load_index()
    while True:
        query = input("\nEnter your search query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break
        results = vector_store.search(query)
        print("\n".join(results) if results else "No relevant results found.")
