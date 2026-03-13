import pdfplumber

def extract_full_text(pdf_path):

    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    lines = full_text.split("\n")

    return full_text, lines