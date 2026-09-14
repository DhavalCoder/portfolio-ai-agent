from fastembed import TextEmbedding
from typing import List

class Embedder:
    def __init__(self):
        """
        Initializes the lightweight embedding model.
        fastembed uses a highly optimized local model (BAAI/bge-small-en-v1.5) 
        that runs without heavy dependencies like PyTorch and costs $0 in API fees.
        """
        self.model = TextEmbedding()

    def embed_text(self, text: str) -> List[float]:
        """
        Converts a single string of text into a mathematical vector (a list of floats).
        """
        # fastembed expects a list of documents and returns a generator
        embeddings_generator = self.model.embed([text])
        embeddings_list = list(embeddings_generator)
        return embeddings_list[0].tolist()

    def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        """
        Converts a list of text chunks into a list of mathematical vectors.
        """
        embeddings_generator = self.model.embed(chunks)
        embeddings_list = list(embeddings_generator)
        return [emb.tolist() for emb in embeddings_list]

# Simple test block
if __name__ == "__main__":
    print("Loading embedding model (this may take a few seconds the very first time)...")
    embedder = Embedder()
    
    sample_text = "Dhaval is a Generative AI Engineer."
    vector = embedder.embed_text(sample_text)
    
    print(f"SUCCESS: Converted text into a vector with {len(vector)} dimensions.")
    print("-" * 40)
    print(f"Original Text: '{sample_text}'")
    print(f"Vector Preview: {vector[:5]} ...")
    print("-" * 40)
