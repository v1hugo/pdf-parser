from datetime import datetime
import unicodedata


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def parse_ordenes(lines, _):
    ordenes_start = next(
        (
            i
            for i, line in enumerate(lines)
            if "relacion de ordenes de corte" in normalize_text(line)
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
                marker in normalize_text(lines[i])
                for marker in [
                    "resumen de seleccion por categoria",
                    "relacion de productos seleccionados",
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
            try:
                row[4] = float(row[4].replace(",", ""))
            except ValueError:
                continue
            try:
                row[2] = datetime.strptime(row[2], "%d/%m/%Y").strftime("%d/%m/%Y")
            except ValueError:
                pass
            ordenes_rows.append(row)
        elif len(row) == 4:
            try:
                row[3] = float(row[3].replace(",", ""))
            except ValueError:
                continue
            try:
                row[1] = datetime.strptime(row[1], "%d/%m/%Y").strftime("%d/%m/%Y")
            except ValueError:
                pass
            ordenes_rows.append([row[0], "", row[1], row[2], row[3]])

    return ordenes_rows, ordenes_total, ordenes_header
