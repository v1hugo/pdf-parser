from datetime import datetime

def parse_ordenes(lines, _):
    ordenes_start = next((i for i, l in enumerate(lines) if "Relación de Ordenes de Corte" in l), -1) + 1
    if ordenes_start == 0:
        return [], 0.0
    ordenes_end = next((i for i in range(ordenes_start, len(lines)) if "Resumen de Seleccion por Categoría" in lines[i] or "Resumen de Selección por Categoría" in lines[i]), len(lines))
    ordenes_header = ['No. de Recepción', 'Ticket', 'Fecha', 'Orden de Corte', 'Kilogramos']
    ordenes_rows = []
    ordenes_total = 0.0
    for line in lines[ordenes_start + 1 : ordenes_end]:
        if line.startswith("Total:"):
            total_parts = line.split()
            ordenes_total = float(total_parts[1].replace(',', ''))
        else:
            row = line.split()
            if len(row) == 5:
                row[4] = float(row[4].replace(',', ''))
                try:
                    dt = datetime.strptime(row[2], '%d/%m/%Y')
                    row[2] = dt.strftime('%d/%m/%Y')
                except ValueError:
                    pass
                ordenes_rows.append(row)
            elif len(row) == 4:
                row[3] = float(row[3].replace(',', ''))
                try:
                    dt = datetime.strptime(row[1], '%d/%m/%Y')
                    row[1] = dt.strftime('%d/%m/%Y')
                except ValueError:
                    pass
                ordenes_rows.append([row[0], '', row[1], row[2], row[3]])
    return ordenes_rows, ordenes_total, ordenes_header
