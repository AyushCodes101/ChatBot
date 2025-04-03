from langchain_openai import OpenAI
from app.services.vector_store import VectorStore
from app.config.logger import logger
from app.config.settings import settings

class Chatbot:
    """Handles user queries using FAISS and OpenAI's LLM."""

    def __init__(self):
        self.vector_store = VectorStore()
        self.vector_store.load_index()
        self.llm = OpenAI(model_name=settings.OPENAI_MODEL)

    def generate_response(self, query):
        """Searches FAISS and generates a response using OpenAI."""
        logger.info(f"Received query: {query}")
        search_results = self.vector_store.search(query)

        if not search_results:
            logger.info("No relevant data found in FAISS.")
            return "Sorry, I do not have any information on that."

        # Construct prompt with retrieved data
        context = "\n".join(search_results)
        prompt = (
            "You are a knowledgeable assistant. Use the following information to answer the user's query. "
            "If the information is not available, do not make up an answer. Instead, say: 'Sorry, I do not have any information on that.'\n\n"
            f"Context:\n{context}\n\nUser Query: {query}\nAnswer:"
        )

        try:
            response = self.llm.invoke(prompt)
            logger.info("Generated response successfully.")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, an error occurred while generating a response."

# If running this file directly, allow interactive chat
if __name__ == "__main__":
    chatbot = Chatbot()
    while True:
        query = input("\nAsk a question (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break
        response = chatbot.generate_response(query)
        print(f"\nChatbot: {response}")
