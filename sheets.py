import os
import gspread
import json
import uuid
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


if "GOOGLE_SERVICE_ACCOUNT" in os.environ:
    creds_json = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])
    CREDS = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
else:
    CREDS = Credentials.from_service_account_file(
        "credentials/service_account.json",
        scopes=SCOPES
    )


client = gspread.authorize(CREDS)

SHEET_NAME = "Avocados Rangel"

def write_to_google_sheets(header, ordenes_rows, ordenes_header, categoria_rows, categoria_header, linea_rows, linea_header, kilos_seleccionados, validation):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = CREDS
    client = gspread.authorize(creds)
    
    sheet_id = '1s1hKC_QRRWELORBc6kDkNwTiqjRO8eaOSKeM30pc2-M'
    spreadsheet = client.open_by_key(sheet_id)
    
    def get_or_create_worksheet(title, rows=100, cols=10):
        try:
            return spreadsheet.worksheet(title)
        except gspread.exceptions.WorksheetNotFound:
            return spreadsheet.add_worksheet(title=title, rows=rows, cols=cols)
    
    seleccion_id = header.get('No. de Selección', str(uuid.uuid4()))

    # Encabezado sheet - Dynamic columns
    encabezado_sheet = get_or_create_worksheet('encabezado', rows=20, cols=20)
    enc_data = encabezado_sheet.get_all_values()
    enc_header = enc_data[0] if enc_data else ['seleccion_id']
    # Add new keys to header if not present
    for key in header.keys():
        if key not in enc_header:
            enc_header.append(key)
    # Update header row if changed
    if len(enc_header) > len(enc_data[0] if enc_data else []):
        encabezado_sheet.update('A1', [enc_header])
    # Map new row values to columns
    enc_row = [None] * len(enc_header)
    enc_row[0] = seleccion_id
    for key, value in header.items():
        if key in enc_header:
            col_idx = enc_header.index(key)
            enc_row[col_idx] = value
    enc_rows_for_id = find_rows_by_id(encabezado_sheet)
    if enc_rows_for_id:
        row_idx = enc_rows_for_id[0]
        encabezado_sheet.update(f'A{row_idx}', [enc_row])
        print(f"Updated encabezado for seleccion_id: {seleccion_id}")
    else:
        encabezado_sheet.append_row(enc_row)
    # Formats
    enc_data_updated = encabezado_sheet.get_all_values()
    num_rows_enc = len(enc_data_updated)
    peso_neto_col = enc_header.index('Peso Neto') + 1 if 'Peso Neto' in enc_header else None
    fecha_col = enc_header.index('Fecha') + 1 if 'Fecha' in enc_header else None
    if peso_neto_col:
        encabezado_sheet.format(f"{chr(64 + peso_neto_col)}2:{chr(64 + peso_neto_col)}{num_rows_enc}", {'numberFormat': {'type': 'NUMBER', 'pattern': '#,##0.00'}})
    if fecha_col:
        encabezado_sheet.format(f"{chr(64 + fecha_col)}2:{chr(64 + fecha_col)}{num_rows_enc}", {'numberFormat': {'type': 'DATE', 'pattern': 'dd/mm/yyyy'}})

    # Ordenes sheet
    ordenes_sheet = get_or_create_worksheet('ordenes', rows=20, cols=7)
    ord_data = ordenes_sheet.get_all_values()
    ord_header = ord_data[0] if ord_data else ['id_orden', 'seleccion_id'] + ordenes_header
    if not ord_data or not ord_data[0]:
        ordenes_sheet.update('A1', [ord_header])
    ord_rows_for_id = find_rows_by_id(ordenes_sheet)
    new_ord_data = []
    for row in ordenes_rows:
        id_orden = str(uuid.uuid4())
        new_ord_data.append([id_orden, seleccion_id] + row)
    if ord_rows_for_id:
        if len(ord_rows_for_id) == len(new_ord_data):
            for idx, row_idx in enumerate(ord_rows_for_id):
                ordenes_sheet.update(f'A{row_idx}', [new_ord_data[idx]])
            print(f"Updated ordenes for seleccion_id: {seleccion_id}")
        else:
            for new_row in new_ord_data:
                ordenes_sheet.append_row(new_row)
    else:
        for new_row in new_ord_data:
            ordenes_sheet.append_row(new_row)
    # Formats
    ord_data_updated = ordenes_sheet.get_all_values()
    num_rows_ord = len(ord_data_updated)
    kilos_col = ord_header.index('Kilogramos') + 1
    fecha_col_ord = ord_header.index('Fecha') + 1
    ordenes_sheet.format(f"{chr(64 + kilos_col)}2:{chr(64 + kilos_col)}{num_rows_ord}", {'numberFormat': {'type': 'NUMBER', 'pattern': '#,##0.00'}})
    ordenes_sheet.format(f"{chr(64 + fecha_col_ord)}2:{chr(64 + fecha_col_ord)}{num_rows_ord}", {'numberFormat': {'type': 'DATE', 'pattern': 'dd/mm/yyyy'}})

    # Detalle sheet
    detalle_sheet = get_or_create_worksheet('detalle', rows=20, cols=5)
    det_data = detalle_sheet.get_all_values()
    det_header = det_data[0] if det_data else ['id_detalle', 'seleccion_id'] + categoria_header
    if not det_data or not det_data[0]:
        detalle_sheet.update('A1', [det_header])
    det_rows_for_id = find_rows_by_id(detalle_sheet)
    new_det_data = []
    for row in categoria_rows:
        id_detalle = str(uuid.uuid4())
        new_det_data.append([id_detalle, seleccion_id] + row)
    if det_rows_for_id:
        if len(det_rows_for_id) == len(new_det_data):
            for idx, row_idx in enumerate(det_rows_for_id):
                detalle_sheet.update(f'A{row_idx}', [new_det_data[idx]])
            print(f"Updated detalle for seleccion_id: {seleccion_id}")
        else:
            for new_row in new_det_data:
                detalle_sheet.append_row(new_row)
    else:
        for new_row in new_det_data:
            detalle_sheet.append_row(new_row)
    # Formats
    det_data_updated = detalle_sheet.get_all_values()
    num_rows_det = len(det_data_updated)
    kilos_col_det = det_header.index('Kilogramos') + 1
    pct_col_det = det_header.index('Porcentaje') + 1
    detalle_sheet.format(f"{chr(64 + kilos_col_det)}2:{chr(64 + kilos_col_det)}{num_rows_det}", {'numberFormat': {'type': 'NUMBER', 'pattern': '#,##0.00'}})
    detalle_sheet.format(f"{chr(64 + pct_col_det)}2:{chr(64 + pct_col_det)}{num_rows_det}", {'numberFormat': {'type': 'PERCENT', 'pattern': '0.00%'}})

    # Resumen sheet
    resumen_sheet = get_or_create_worksheet('resumen', rows=20, cols=5)
    res_data = resumen_sheet.get_all_values()
    res_header = res_data[0] if res_data else ['id_resumen', 'seleccion_id'] + linea_header
    if not res_data or not res_data[0]:
        resumen_sheet.update('A1', [res_header])
    res_rows_for_id = find_rows_by_id(resumen_sheet)
    new_res_data = []
    for row in linea_rows:
        id_resumen = str(uuid.uuid4())
        new_res_data.append([id_resumen, seleccion_id] + row)
    if res_rows_for_id:
        if len(res_rows_for_id) == len(new_res_data):
            for idx, row_idx in enumerate(res_rows_for_id):
                resumen_sheet.update(f'A{row_idx}', [new_res_data[idx]])
            print(f"Updated resumen for seleccion_id: {seleccion_id}")
        else:
            for new_row in new_res_data:
                resumen_sheet.append_row(new_row)
    else:
        for new_row in new_res_data:
            resumen_sheet.append_row(new_row)
    # Append or update extras
    res_data_updated = resumen_sheet.get_all_values()
    has_kilos = any('Kilogramos Seleccionados' in row for row in res_data_updated)
    has_validation = any('Validation' in row for row in res_data_updated)
#    if not has_kilos:
#        resumen_sheet.append_row(['Kilogramos Seleccionados', kilos_seleccionados])
#    if not has_validation:
#        resumen_sheet.append_row(['Validation', validation])
    # Formats
    num_rows_res = len(res_data_updated)
    kilos_col_res = res_header.index('Kilogramos') + 1
    pct_col_res = res_header.index('Porcentaje') + 1
    resumen_sheet.format(f"{chr(64 + kilos_col_res)}2:{chr(64 + kilos_col_res)}{num_rows_res}", {'numberFormat': {'type': 'NUMBER', 'pattern': '#,##0.00'}})
    resumen_sheet.format(f"{chr(64 + pct_col_res)}2:{chr(64 + pct_col_res)}{num_rows_res}", {'numberFormat': {'type': 'PERCENT', 'pattern': '0.00%'}})
    resumen_sheet.format(f"B{num_rows_res + 1}", {'numberFormat': {'type': 'NUMBER', 'pattern': '#,##0.00'}})  # Kilos Seleccionados

def find_rows_by_id(sheet, id_col=2, seleccion_id=''):
    data = sheet.get_all_values()
    rows_for_id = []
    for row_idx, row in enumerate(data, start=1):
        if row and len(row) >= id_col and row[id_col - 1] == seleccion_id:
            rows_for_id.append(row_idx)
    return rows_for_id
