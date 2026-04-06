import re


def parse_lineas(lines):
    linea_start = next(
        (
            i
            for i, line in enumerate(lines)
            if "Resumen de Selección por Línea de Producto" in line
            or "Resumen de Seleccion por Linea de Producto" in line
        ),
        -1,
    ) + 1

    if linea_start == 0:
        return [], []

    linea_end = next(
        (i for i in range(linea_start, len(lines)) if "Kilogramos Seleccionados:" in lines[i]),
        len(lines),
    )
    linea_header = ["Línea de Producto", "Kilogramos", "Porcentaje"]
    linea_rows = []
    pattern = r"^(.*?)\s+([-]?\d{1,3}(?:,\d{3})*\.\d{2})\s+([-]?\d{1,3}(?:,\d{3})*\.\d{2}\s?%)$"

    for line in lines[linea_start + 1 : linea_end]:
        if any(
            text in line
            for text in [
                "Fecha:",
                "Página:",
                "Reporte de Selección",
                "Kilogramos Seleccionados:",
                "Kilogramos por Seleccionar:",
            ]
        ):
            continue

        match = re.match(pattern, line)
        if not match:
            continue

        linea = match.group(1).strip()
        kg = float(match.group(2).replace(",", ""))
        pct_str = match.group(3).rstrip("%").strip()
        pct = float(pct_str.replace(",", "")) / 100
        linea_rows.append([linea, kg, pct])

    return linea_rows, linea_header
