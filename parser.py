import logging

from utils.pdf_extract import extract_full_text
from utils.parse_header import parse_header
from utils.parse_ordenes import parse_ordenes
from utils.parse_categorias import parse_categorias
from utils.parse_lineas import parse_lineas
from utils.parse_extras import parse_extras
from tabulate import tabulate

from sheets import write_to_google_sheets



def main(pdf_path):
    print("Processing PDF:", pdf_path)

    full_text, lines = extract_full_text(pdf_path)

    header, _ = parse_header(lines)
#    print("Header extracted:", header)

    ordenes_rows, ordenes_total, ordenes_header = parse_ordenes(lines, None)
    categoria_rows, categoria_total, categoria_header = parse_categorias(lines)
    linea_rows, linea_header = parse_lineas(lines)
    kilos_seleccionados, kilos_por_seleccionar = parse_extras(lines)
    peso_neto = header.get('Peso Neto', 0.0)
    orders_sum = sum(float(row[-1]) for row in ordenes_rows) if ordenes_rows else 0
    categoria_sum = sum(float(row[1]) for row in categoria_rows) if categoria_rows else 0

    validation_ok = all([
        abs(peso_neto - ordenes_total) < 0.01,
        abs(peso_neto - categoria_total) < 0.01,
        abs(peso_neto - orders_sum) < 0.01,
        abs(peso_neto - categoria_sum) < 0.01,
        abs(peso_neto - kilos_seleccionados) < 0.01
    ])

    validation = "OK" if validation_ok else "ERROR"

    print("contenido: ",header)
#    logging.info(tabulate(header, tablefmt="psql"))

    write_to_google_sheets(header,ordenes_rows,ordenes_header,categoria_rows,categoria_header,linea_rows,linea_header,kilos_seleccionados,validation)

    return {
        "header": header,
        "validation": validation
    }