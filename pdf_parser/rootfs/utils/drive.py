import io
import json
import os

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from addon_config import get_option, require_option


SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_credentials():
    service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT")
    if service_account_json:
        creds_json = json.loads(service_account_json)
        return Credentials.from_service_account_info(creds_json, scopes=SCOPES)

    service_account_path = require_option("service_account_path")
    return Credentials.from_service_account_file(service_account_path, scopes=SCOPES)


CREDS = get_credentials()
drive_service = build("drive", "v3", credentials=CREDS)

FOLDER_ENTRADA = require_option("folder_entrada")
FOLDER_PROCESADOS = require_option("folder_procesados")
FOLDER_ERROR = require_option("folder_error")


def list_pdfs(folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get("files", [])


def download_file_to_memory(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    while not done:
        _, done = downloader.next_chunk()

    fh.seek(0)
    return fh


def move_file(file_id, new_folder_id, new_file_name=None):
    file = drive_service.files().get(fileId=file_id, fields="parents").execute()
    previous_parents = ",".join(file.get("parents", []))
    update_body = {}

    if new_file_name:
        update_body["name"] = f"Reporte_{new_file_name}"

    drive_service.files().update(
        fileId=file_id,
        addParents=new_folder_id,
        removeParents=previous_parents,
        body=update_body if update_body else None,
    ).execute()


def get_file_url(file_id):
    return f"https://drive.google.com/file/d/{file_id}/view"


def get_or_create_worksheet(spreadsheet, title, rows=100, cols=10):
    try:
        return spreadsheet.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=title, rows=rows, cols=cols)
