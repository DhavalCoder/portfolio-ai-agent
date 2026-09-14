import os
import sys

# Add project root to Python path so we can import our app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag.loader import extract_text_from_pdf
from app.rag.splitter import chunk_text
from app.rag.embeddings import Embedder
from app.rag.vector_store import SimpleVectorStore

# The exact path you provided in your original instructions
DEFAULT_PDF_PATH = r"C:\Users\Dhawal\Downloads\Dhaval_Chorwadkar_GenAI_Engineer.pdf"

def main(pdf_path=DEFAULT_PDF_PATH):
    print(f"Starting ingestion process for: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: Could not find the PDF at {pdf_path}")
        print("Please check the file path and try again.")
        sys.exit(1)

    print("1. Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("Failed to extract text. Is the PDF empty?")
        sys.exit(1)
        
    print("2. Chunking text into smaller logical pieces...")
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    print(f"   Created {len(chunks)} chunks.")

    print("3. Generating mathematical vector embeddings (this might take a few seconds)...")
    embedder = Embedder()
    embeddings = embedder.embed_chunks(chunks)
    
    print("4. Saving to the custom Local Vector Database...")
    vector_store = SimpleVectorStore()
    vector_store.add_chunks(chunks, embeddings)
    
    print("SUCCESS! Your resume has been completely ingested and the AI brain is fully loaded.")

if __name__ == "__main__":
    main()
