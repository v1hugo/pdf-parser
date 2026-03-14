import pdfplumber

def extract_full_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    return full_text, lines