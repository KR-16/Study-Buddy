from pypdf import PdfReader
import re
import time

def clean_text(text):
    """
    Remove extra white spaces and special characters
    """
    text = re.sub(r"\s+", " ", text)        # collapse whitespace
    return text.strip()

def extract_pdf_text(pdf_path):
    """
    Extract and clean the PDF
    """

    print(f"Processing {pdf_path}...")
    start = time.time()
    reader = PdfReader(pdf_path)
    
    return clean_text(" ".join([page.extract_text() for page in reader.pages]))

if __name__ == "__main__":
    extracted = extract_pdf_text()
    print(f"Extracted {len(extracted)}  characters:\n {extracted[:500]}...")