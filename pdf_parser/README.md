# PDF Parser Add-on

Home Assistant add-on that reads PDFs from Google Drive, parses their contents, and writes the output to Google Sheets.

## Configuration

Use the add-on options to set:

- `spreadsheet_id`
- `folder_entrada`
- `folder_procesados`
- `folder_error`
- `service_account_path`
- `poll_interval_seconds`

Place your Google service account JSON at the configured path inside Home Assistant, for example:

`/config/pdf_parser/service_account.json`

The add-on definition is stored in `config.yaml`.

`poll_interval_seconds` controls how often the add-on checks Google Drive for new PDFs while staying alive in the background. The default is `60`.
