from datetime import datetime

def parse_header(lines):
    header = {}
    header_end = -1
    for i, line in enumerate(lines):
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ''
            # Convert specific fields
            if key == 'Peso Neto':
                value = float(value.replace(',', ''))
            elif key == 'Fecha':
                try:
                    dt = datetime.strptime(value, '%d/%m/%Y')
                    value = dt.strftime('%d/%m/%Y')
                except ValueError:
                    pass
            header[key] = value
        if "Relación de Ordenes de Corte" in line:
            header_end = i
            break
    return header, header_end
