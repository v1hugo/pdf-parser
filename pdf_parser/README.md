# PDF Parser Add-on

Home Assistant add-on that reads PDFs from Google Drive, parses their contents, and writes the output to Google Sheets.

## Configuration

Use the add-on options to set:

- `spreadsheet_id`
- `folder_entrada`
- `folder_procesados`
- `folder_error`
- `service_account_path`

Place your Google service account JSON at the configured path inside Home Assistant, for example:

`/config/pdf_parser/service_account.json`
