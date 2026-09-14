import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Reads a PDF file and extracts all text from it, page by page.
    Returns the concatenated text.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
        
    reader = PdfReader(pdf_path)
    extracted_text = []
    
    # Handle multiple pages
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            extracted_text.append(text)
            
    # Join all pages with double newlines to maintain paragraph separation
    full_text = "\n\n".join(extracted_text)
    
    # Basic cleanup: remove excessive whitespace
    full_text = " ".join(full_text.split())
    
    return full_text

# Simple test block that runs only if this file is executed directly
if __name__ == "__main__":
    test_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "resume.pdf")
    test_path = os.path.abspath(test_path)
    
    try:
        text = extract_text_from_pdf(test_path)
        print(f"SUCCESS: Extracted {len(text)} characters from the PDF.")
        print("-" * 40)
        print("First 200 characters preview:")
        print(text[:200].encode('ascii', 'replace').decode('ascii'))
        print("-" * 40)
    except Exception as e:
        print(f"ERROR extracting PDF: {e}")
