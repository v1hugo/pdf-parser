import os
import gspread
import json
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_json = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])

CREDS = Credentials.from_service_account_info(
    creds_json,
    scopes=SCOPES
)

client = gspread.authorize(CREDS)

SHEET_NAME = "PDF_DATA"

def write_to_google_sheets(header,
                           ordenes_rows,
                           ordenes_header,
                           categoria_rows,
                           categoria_header,
                           linea_rows,
                           linea_header,
                           kilos,
                           validation):

    sheet = client.open(SHEET_NAME).sheet1

    row = [
        header.get("Cliente",""),
        header.get("Fecha",""),
        header.get("Peso Neto",0),
        kilos,
        validation
    ]

    sheet.append_row(row)