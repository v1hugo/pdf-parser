# PDF Drive Parser

Sistema para procesar PDFs desde Google Drive y enviar datos a Google Sheets.

Arquitectura:

Google Drive
↓
Apps Script
↓
API Flask (Render)
↓
Parser
↓
Google Sheets

Endpoint:

POST /process_pdf