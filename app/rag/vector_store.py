import json
import os
import math
from typing import List

class SimpleVectorStore:
    def __init__(self, persist_path: str = "data/vector_index.json"):
        """
        Initializes the vector store. 
        It attempts to load existing data from a JSON file so we don't 
        lose our data when the FastAPI server restarts.
        """
        # Get the absolute path to the data folder
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.persist_path = os.path.join(base_dir, persist_path)
        
        self.documents = []  # Will hold dicts: {"text": str, "vector": List[float]}
        self._load()

    def add_chunks(self, chunks: List[str], embeddings: List[List[float]]):
        """
        Pairs up the raw text chunks with their mathematical vectors and saves them.
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings.")
        
        for chunk, vector in zip(chunks, embeddings):
            self.documents.append({
                "text": chunk,
                "vector": vector
            })
        self._save()

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculates how similar two vectors are using basic math.
        Returns a score between -1.0 (opposite) and 1.0 (identical).
        """
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def search(self, query_vector: List[float], top_k: int = 3) -> List[str]:
        """
        Compares the user's question vector against every resume chunk vector.
        Returns the top_k most similar text chunks.
        """
        if not self.documents:
            return []
            
        # Calculate similarity score for every document in our database
        scored_docs = []
        for doc in self.documents:
            score = self._cosine_similarity(query_vector, doc["vector"])
            scored_docs.append((score, doc["text"]))
            
        # Sort by highest score first (closest match)
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        # Return just the raw text of the top_k results
        return [doc_text for score, doc_text in scored_docs[:top_k]]

    def _save(self):
        """Saves the database to a plain JSON file so you can inspect it."""
        with open(self.persist_path, "w", encoding="utf-8") as f:
            json.dump(self.documents, f, indent=2)

    def _load(self):
        """Loads the database from the JSON file if it exists."""
        if os.path.exists(self.persist_path):
            with open(self.persist_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)

# Test block
if __name__ == "__main__":
    print("Testing Vector Store...")
    store = SimpleVectorStore("data/test_index.json")
    
    # Mock data
    store.add_chunks(["I love Python", "I eat apples"], [[1.0, 0.0], [0.0, 1.0]])
    
    # Search for something close to [1.0, 0.0]
    results = store.search([0.9, 0.1], top_k=1)
    print(f"Top match: {results[0]}")
