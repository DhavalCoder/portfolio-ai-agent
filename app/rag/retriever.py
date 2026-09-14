import os
import sys

# Ensure we can import from the app module when running directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.rag.embeddings import Embedder
from app.rag.vector_store import SimpleVectorStore

class ResumeRetriever:
    def __init__(self):
        """
        Initializes the retriever by bringing together our two previous stages:
        the Embedding model and the Vector Store.
        """
        self.embedder = Embedder()
        self.vector_store = SimpleVectorStore()

    def retrieve_context(self, question: str, top_k: int = 3) -> str:
        """
        Takes a user's question, searches the vector store, 
        and returns the most relevant resume chunks combined into a single string.
        """
        # Step 1: Convert the user's question into a mathematical vector
        query_vector = self.embedder.embed_text(question)
        
        # Step 2: Perform the mathematical similarity search
        matching_chunks = self.vector_store.search(query_vector, top_k=top_k)
        
        # Step 3: Format the results so the LLM can read them easily
        if not matching_chunks:
            return "No relevant context found in the resume."
            
        combined_context = "\n\n---\n\n".join(matching_chunks)
        return combined_context

# Test block
if __name__ == "__main__":
    print("Testing Retriever Orchestration...")
    retriever = ResumeRetriever()
    
    question = "What backend technologies does Dhaval know?"
    print(f"\nQuestion: {question}")
    print("\nRetrieving Context...\n")
    
    context = retriever.retrieve_context(question)
    
    # We slice to 300 characters just for the terminal preview
    print(context[:300].encode('ascii', 'replace').decode('ascii') + "...\n")
