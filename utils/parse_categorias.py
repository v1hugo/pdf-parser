from datetime import datetime
import re

def parse_categorias(lines):
    categoria_start = next((i for i, l in enumerate(lines) if "Resumen de Seleccion por Categoría" in l or "Resumen de Selección por Categoría" in l), -1) + 1
    if categoria_start == 0:
        return [], 0.0
    categoria_end = next((i for i in range(categoria_start, len(lines)) if "Resumen de Selección por Línea de Producto" in lines[i] or "Resumen de Seleccion por Linea de Producto" in lines[i]), len(lines))
    categoria_header = ['Categoría', 'Kilogramos', 'Porcentaje']
    categoria_rows = []
    categoria_total = 0.0
    pattern = r'^(.*?)\s+([\d,]+\.\d{2})\s+([-]?\d{1,3}(?:,\d{3})*\.\d{2}\s?%)$'
    for line in lines[categoria_start + 1 : categoria_end]:
        if line.startswith("Total:"):
            total_match = re.search(r'Total:\s+([\d,]+\.\d{2})\s+([\d.]+ %)', line)
            if total_match:
                categoria_total = float(total_match.group(1).replace(',', ''))
        else:
            match = re.match(pattern, line)
            if match:
                categoria = match.group(1).strip()
                kg = float(match.group(2).replace(',', ''))
                pct_str = match.group(3).rstrip('%').strip()
                pct = float(pct_str.replace(',', '')) / 100
                categoria_rows.append([categoria, kg, pct])
    return categoria_rows, categoria_total, categoria_header
