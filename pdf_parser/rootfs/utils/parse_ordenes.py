from datetime import datetime


def parse_ordenes(lines, _):
    ordenes_start = next(
        (
            i
            for i, line in enumerate(lines)
            if "Relacion de Ordenes de Corte" in line or "Relación de Ordenes de Corte" in line
        ),
        -1,
    ) + 1

    if ordenes_start == 0:
        return [], 0.0, []

    ordenes_end = next(
        (
            i
            for i in range(ordenes_start, len(lines))
            if any(
                marker in lines[i]
                for marker in [
                    "Resumen de Seleccion por Categoria",
                    "Resumen de Selección por Categoría",
                    "Relacion de Productos Seleccionados",
                    "Relación de Productos Seleccionados",
                ]
            )
        ),
        len(lines),
    )

    ordenes_header = [
        "No. de Recepción",
        "Ticket",
        "Fecha",
        "Orden de Corte",
        "Kilogramos",
    ]

    ordenes_rows = []
    ordenes_total = 0.0

    for line in lines[ordenes_start + 1 : ordenes_end]:
        row = line.strip().split()

        if line.startswith("Total:"):
            total_parts = line.split()
            if len(total_parts) > 1:
                ordenes_total = float(total_parts[1].replace(",", ""))
            continue

        if len(row) == 5:
            row[4] = float(row[4].replace(",", ""))
            try:
                row[2] = datetime.strptime(row[2], "%d/%m/%Y").strftime("%d/%m/%Y")
            except ValueError:
                pass
            ordenes_rows.append(row)
        elif len(row) == 4:
            row[3] = float(row[3].replace(",", ""))
            try:
                row[1] = datetime.strptime(row[1], "%d/%m/%Y").strftime("%d/%m/%Y")
            except ValueError:
                pass
            ordenes_rows.append([row[0], "", row[1], row[2], row[3]])

    return ordenes_rows, ordenes_total, ordenes_header
