import os
from app.services.scraper import Scraper
from app.services.vector_store import VectorStore
from app.services.chat import Chatbot
from app.config.logger import logger

def main():
    """Main function to run the RAG chatbot."""
    print("\n🔹 Welcome to the RAG Chatbot! 🔹")
    website_url = input("Enter the website URL to scrape: ").strip() 

    # Ensure the scraped data folder exists
    os.makedirs("app/data", exist_ok=True)

    # Check if scraped data already exists
    scraped_data_path = os.path.join("app/data", "scraped_data.json")
    if not os.path.exists(scraped_data_path):
        print("\n🔄 Scraping website...")
        scraper = Scraper(website_url)
        scraped_data = scraper.scrape()
        if not scraped_data:
            print("\n❌ Scraping failed. Exiting...")
            return
        print("✅ Scraping completed successfully!")
    else:
        print("\n📂 Using previously scraped data.")

    # Initialize FAISS vector store
    vector_store = VectorStore()
    if not os.path.exists("app/faiss_index/index.faiss"):
        print("\n🔄 Creating FAISS index...")
        vector_store.create_index()
        print("✅ FAISS index created successfully!")
    else:
        print("\n📂 Loading existing FAISS index...")
        vector_store.load_index()

    # Initialize chatbot
    chatbot = Chatbot()

    # Start interactive chat
    print("\n💬 You can now ask questions. Type 'exit' to quit.")
    while True:
        query = input("\nAsk a question: ").strip()
        if query.lower() == "exit":
            print("\n👋 Exiting chatbot. Goodbye!")
            break
        response = chatbot.generate_response(query)
        print(f"\nChatbot: {response}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print("\n❌ An unexpected error occurred. Check logs for details.")
