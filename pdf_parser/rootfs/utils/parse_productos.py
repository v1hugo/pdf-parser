import re


def parse_productos(lines):
    start = None
    rows = []
    total_kg = 0.0

    for i, line in enumerate(lines):
        if (
            "Relacion de Productos Seleccionados" in line
            or "Relación de Productos Seleccionados" in line
        ):
            start = i + 2
            break

    if start is None:
        return [], 0.0, []

    for i in range(start, len(lines)):
        line = lines[i].strip()

        if line.startswith("Total:"):
            parts = re.findall(r"[\d,]+\.\d+", line)
            if parts:
                total_kg = float(parts[-1].replace(",", ""))
            break

        matches = re.findall(r"[\d,]+\.\d+", line)
        if len(matches) < 2:
            continue

        cantidad = float(matches[-2].replace(",", ""))
        kg = float(matches[-1].replace(",", ""))
        descripcion = line[: line.rfind(matches[-2])].strip()

        categoria = None
        if "CAT 1" in descripcion:
            categoria = "CAT 1"
        elif "CAT 2" in descripcion:
            categoria = "CAT 2"

        rows.append([descripcion, kg, cantidad, categoria, None])

    header = ["Categoría", "Kilogramos", "Cantidad", "Tipo", "Porcentaje"]
    return rows, total_kg, header
