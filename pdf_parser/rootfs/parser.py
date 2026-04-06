import unicodedata

from sheets import write_to_google_sheets
from utils.parse_categorias import parse_categorias
from utils.parse_extras import parse_extras
from utils.parse_header import parse_header
from utils.parse_lineas import parse_lineas
from utils.parse_ordenes import parse_ordenes
from utils.parse_productos import parse_productos
from utils.pdf_extract import extract_full_text


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def detect_document_type(lines):
    for line in lines:
        norm = normalize_text(line)

        if "relacion de productos seleccionados" in norm:
            return "PRODUCTOS"

        if "resumen de seleccion por categoria" in norm:
            return "CATEGORIA"

    return "UNKNOWN"


def add_porcentaje(rows, total_kg, has_porcentaje=False):
    if not rows or has_porcentaje:
        return rows

    acumulado = 0.0

    for i, row in enumerate(rows):
        kg = float(row[1])

        if i < len(rows) - 1:
            porcentaje = round((kg / total_kg) if total_kg > 0 else 0.0, 4)
            acumulado += porcentaje
        else:
            porcentaje = round(1.0 - acumulado, 4)

        while len(row) <= 4:
            row.append(None)

        row[4] = porcentaje

    return rows


PALABRAS_RESTA = ["MERMA", "VAR", "VARIACION"]


def es_merma(descripcion):
    desc = descripcion.upper()
    return any(p in desc for p in PALABRAS_RESTA)


def calcular_categoria_sum(categoria_rows, peso_neto):
    base = 0.0
    merma_total = 0.0

    for row in categoria_rows:
        descripcion = row[0]
        kg = float(row[1])

        if es_merma(descripcion):
            merma_total += abs(kg)
        else:
            base += kg

    total_sumando = base + merma_total
    total_restando = base - merma_total

    if abs(total_sumando - peso_neto) < abs(total_restando - peso_neto):
        return total_sumando

    return total_restando


def main(file_stream, file_url=None):
    print("Processing PDF...")

    _, lines = extract_full_text(file_stream)
    doc_type = detect_document_type(lines)
    print(f"Document type: {doc_type}")

    header, _ = parse_header(lines)

    reporte_id = str(
        header.get("No. de Seleccion", header.get("No. de Selección", ""))
    ).zfill(7)
    header["PDF_URL"] = (
        f'=HYPERLINK("{file_url}", "{reporte_id}")' if file_url else reporte_id
    )

    ordenes_rows, ordenes_total, ordenes_header = parse_ordenes(lines, None)

    if doc_type == "CATEGORIA":
        categoria_rows, categoria_total, categoria_header = parse_categorias(lines)
    elif doc_type == "PRODUCTOS":
        categoria_rows, categoria_total, categoria_header = parse_productos(lines)
    else:
        raise ValueError("Unsupported document type")

    categoria_rows = add_porcentaje(
        categoria_rows,
        categoria_total,
        has_porcentaje=(doc_type == "CATEGORIA"),
    )

    linea_rows, linea_header = parse_lineas(lines)
    kilos_seleccionados, _ = parse_extras(lines)

    try:
        peso_neto = float(str(header.get("Peso Neto", 0)).replace(",", ""))
    except Exception:
        peso_neto = 0.0

    orders_sum = sum(float(row[-1]) for row in ordenes_rows) if ordenes_rows else 0.0
    categoria_sum = calcular_categoria_sum(categoria_rows, peso_neto) if categoria_rows else 0.0

    validation_ok = all(
        [
            abs(peso_neto - ordenes_total) < 0.01,
            abs(peso_neto - categoria_total) < 0.01,
            abs(peso_neto - orders_sum) < 0.01,
            abs(peso_neto - categoria_sum) < 0.01,
            abs(peso_neto - kilos_seleccionados) < 0.01,
        ]
    )

    validation = "OK" if validation_ok else "ERROR"

    result = write_to_google_sheets(
        header,
        ordenes_rows,
        ordenes_header,
        categoria_rows,
        categoria_header,
        linea_rows,
        linea_header,
        kilos_seleccionados,
        validation,
    )

    if result["status"] == "exists":
        print(f"Duplicate record: {result['seleccion_id']}")
        return {
            "status": "exists",
            "seleccion_id": result["seleccion_id"],
            "message": result["message"],
            "doc_type": doc_type,
        }

    return {
        "status": "success",
        "seleccion_id": result["seleccion_id"],
        "header": header,
        "validation": validation,
        "doc_type": doc_type,
    }
