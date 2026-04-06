import re


def parse_categorias(lines):
    categoria_start = next(
        (
            i
            for i, line in enumerate(lines)
            if "Resumen de Seleccion por Categoria" in line
            or "Resumen de Selección por Categoría" in line
        ),
        -1,
    ) + 1

    if categoria_start == 0:
        return [], 0.0, []

    categoria_end = next(
        (
            i
            for i in range(categoria_start, len(lines))
            if "Resumen de Seleccion por Linea de Producto" in lines[i]
            or "Resumen de Selección por Línea de Producto" in lines[i]
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
