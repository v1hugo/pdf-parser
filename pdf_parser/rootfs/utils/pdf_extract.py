import pdfplumber

def extract_full_text(file_stream):
    # 👇 MUY IMPORTANTE: asegurar que el puntero esté al inicio
    file_stream.seek(0)

    with pdfplumber.open(file_stream) as pdf:
        full_text = "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )

    lines = [line.strip() for line in full_text.split('\n') if line.strip()]

    return full_text, lines