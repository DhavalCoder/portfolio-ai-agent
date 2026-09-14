from typing import List

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Splits a large text string into smaller chunks.
    
    Args:
        text: The full text to split.
        chunk_size: Maximum number of characters per chunk.
        overlap: Number of characters to overlap between consecutive chunks.
        
    Returns:
        A list of text chunks.
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        # Define the end of the current chunk
        end = start + chunk_size
        chunk = text[start:end]
        
        # Don't add completely empty chunks
        if chunk.strip():
            chunks.append(chunk.strip())
            
        # Move the start pointer forward, stepping back by the overlap amount
        start += (chunk_size - overlap)

    return chunks

# Test block
if __name__ == "__main__":
    import os
    import sys
    
    # Add parent directory to path so we can import the loader
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from app.rag.loader import extract_text_from_pdf
    
    test_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "resume.pdf")
    test_path = os.path.abspath(test_path)
    
    try:
        raw_text = extract_text_from_pdf(test_path)
        chunks = chunk_text(raw_text, chunk_size=500, overlap=50)
        
        print(f"SUCCESS: Split resume into {len(chunks)} chunks.")
        print("-" * 40)
        print(f"Preview of Chunk 1 ({len(chunks[0])} chars):")
        print(chunks[0].encode('ascii', 'replace').decode('ascii'))
        print("-" * 40)
        print(f"Preview of Chunk 2 ({len(chunks[1])} chars):")
        print(chunks[1].encode('ascii', 'replace').decode('ascii'))
        print("-" * 40)
    except Exception as e:
        print(f"ERROR: {e}")
