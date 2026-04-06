import re
import unicodedata


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def parse_categorias(lines):
    categoria_start = next(
        (
            i
            for i, line in enumerate(lines)
            if "resumen de seleccion por categoria" in normalize_text(line)
        ),
        -1,
    ) + 1

    if categoria_start == 0:
        return [], 0.0, []

    categoria_end = next(
        (
            i
            for i in range(categoria_start, len(lines))
            if "resumen de seleccion por linea de producto" in normalize_text(lines[i])
        ),
        len(lines),
    )

    categoria_header = [
        "Categoría",
        "Kilogramos",
        "Cantidad",
        "Tipo",
        "Porcentaje",
    ]

    categoria_rows = []
    categoria_total = 0.0
    pattern = r"^(.*?)\s+([\d,]+\.\d{2})\s+([-]?\d{1,3}(?:,\d{3})*\.\d{2}\s?%)$"

    for line in lines[categoria_start + 1 : categoria_end]:
        if line.startswith("Total:"):
            total_match = re.search(r"Total:\s+([\d,]+\.\d{2})\s+([\d.]+ %)", line)
            if total_match:
                categoria_total = float(total_match.group(1).replace(",", ""))
            continue

        match = re.match(pattern, line)
        if not match:
            continue

        categoria = match.group(1).strip()
        kg = float(match.group(2).replace(",", ""))
        pct_str = match.group(3).rstrip("%").strip()
        pct = float(pct_str.replace(",", "")) / 100
        categoria_rows.append([categoria, kg, None, None, pct])

    return categoria_rows, categoria_total, categoria_header
