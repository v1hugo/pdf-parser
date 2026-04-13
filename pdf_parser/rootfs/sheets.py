from datetime import datetime, timezone
import uuid

import gspread

from addon_config import require_option
from utils.drive import CREDS, get_or_create_worksheet


ENCABEZADO_COLUMNS = [
    "seleccion_id",
    "No. de Selección",
    "Fecha",
    "No. de Lote",
    "Referencia",
    "Productor",
    "Huerta",
    "Registro",
    "G.G.N.",
    "Jefe de Acopio",
    "Tipo de Corte",
    "Peso Neto",
    "Observaciones",
    "PDF_URL",
]

LOG_COLUMNS = [
    "timestamp",
    "file_name",
    "file_id",
    "file_url",
    "status",
    "validation",
    "seleccion_id",
    "doc_type",
    "message",
]


def open_spreadsheet():
    spreadsheet_id = require_option("spreadsheet_id")
    client = gspread.authorize(CREDS)
    return client.open_by_key(spreadsheet_id)


def seleccion_id_exists(sheet, seleccion_id):
    data = sheet.get_all_values()

    if not data:
        return False

    header = data[0]

    if "seleccion_id" not in header:
        return False

    col_idx = header.index("seleccion_id")

    for row in data[1:]:
        if len(row) > col_idx and str(row[col_idx]) == str(seleccion_id):
            return True

    return False


def write_encabezado(spreadsheet, header, seleccion_id):
    sheet = get_or_create_worksheet(spreadsheet, "encabezado", 20, 20)
    row = []

    for col in ENCABEZADO_COLUMNS:
        row.append(seleccion_id if col == "seleccion_id" else header.get(col))

    sheet.append_row(row, value_input_option="USER_ENTERED")


def write_ordenes(spreadsheet, ordenes_rows, ordenes_header, seleccion_id):
    sheet = get_or_create_worksheet(spreadsheet, "ordenes", 20, 7)
    data = sheet.get_all_values()
    header = data[0] if data else ["id_orden", "seleccion_id"] + ordenes_header

    if not data:
        sheet.update("A1", [header])

    for row in ordenes_rows:
        sheet.append_row([str(uuid.uuid4()), seleccion_id] + row)


def write_detalle(spreadsheet, categoria_rows, categoria_header, seleccion_id):
    sheet = get_or_create_worksheet(spreadsheet, "detalle", 20, 5)
    data = sheet.get_all_values()
    header = data[0] if data else ["id_detalle", "seleccion_id"] + categoria_header

    if not data:
        sheet.update("A1", [header])

    for row in categoria_rows:
        new_row = [None] * len(header)
        new_row[header.index("id_detalle")] = str(uuid.uuid4())
        new_row[header.index("seleccion_id")] = seleccion_id

        if "Categoría" in header:
            new_row[header.index("Categoría")] = row[0]

        if "Kilogramos" in header:
            new_row[header.index("Kilogramos")] = float(row[1])

        if "Porcentaje" in header and len(row) > 4 and row[4] is not None:
            new_row[header.index("Porcentaje")] = float(row[4])

        sheet.append_row(new_row)


def write_resumen(spreadsheet, linea_rows, linea_header, seleccion_id):
    sheet = get_or_create_worksheet(spreadsheet, "resumen", 20, 5)
    data = sheet.get_all_values()
    header = data[0] if data else ["id_resumen", "seleccion_id"] + linea_header

    if not data:
        sheet.update("A1", [header])

    for row in linea_rows:
        sheet.append_row([str(uuid.uuid4()), seleccion_id] + row)


def write_to_google_sheets(
    header,
    ordenes_rows,
    ordenes_header,
    categoria_rows,
    categoria_header,
    linea_rows,
    linea_header,
    kilos_seleccionados,
    validation,
):
    del kilos_seleccionados
    del validation

    spreadsheet = open_spreadsheet()

    seleccion_id = str(
        header.get("No. de Selección", header.get("No. de Seleccion", str(uuid.uuid4())))
    )

    encabezado_sheet = get_or_create_worksheet(spreadsheet, "encabezado", 20, 20)

    if seleccion_id_exists(encabezado_sheet, seleccion_id):
        return {
            "status": "exists",
            "seleccion_id": seleccion_id,
            "message": "Record already exists",
        }

    write_encabezado(spreadsheet, header, seleccion_id)
    write_ordenes(spreadsheet, ordenes_rows, ordenes_header, seleccion_id)
    write_detalle(spreadsheet, categoria_rows, categoria_header, seleccion_id)
    write_resumen(spreadsheet, linea_rows, linea_header, seleccion_id)

    return {
        "status": "success",
        "seleccion_id": seleccion_id,
        "message": "Record saved",
    }


def append_process_log(file_name, file_id, file_url, result=None, error=None):
    spreadsheet = open_spreadsheet()
    sheet = get_or_create_worksheet(spreadsheet, "logs", 20, len(LOG_COLUMNS))
    data = sheet.get_all_values()

    if not data:
        sheet.update("A1", [LOG_COLUMNS])

    result = result or {}
    message = str(error) if error is not None else result.get("message", "")

    row = [
        datetime.now(timezone.utc).isoformat(),
        file_name,
        file_id,
        file_url or "",
        result.get("status", "error" if error is not None else ""),
        result.get("validation", ""),
        result.get("seleccion_id", ""),
        result.get("doc_type", ""),
        message,
    ]
    sheet.append_row(row, value_input_option="USER_ENTERED")
