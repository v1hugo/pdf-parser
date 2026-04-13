# PDF Parser Add-on

Home Assistant add-on that reads PDFs from Google Drive, parses their contents, and writes the output to Google Sheets.

Current add-on version: `1.0.2`

See [CHANGELOG.md](CHANGELOG.md) for the list of improvements in this release.

## Configuration

Use the add-on options to set:

- `spreadsheet_id`
- `folder_entrada`
- `folder_procesados`
- `folder_error`
- `service_account_path`
- `poll_interval_seconds`
- `mqtt_host` (optional)
- `mqtt_port` (optional)
- `mqtt_topic` (optional)
- `mqtt_username` (optional)
- `mqtt_password` (optional)

Place your Google service account JSON at the configured path inside Home Assistant, for example:

`/config/pdf_parser/service_account.json`

The add-on definition is stored in `config.yaml`.

`poll_interval_seconds` controls how often the add-on checks Google Drive for new PDFs while staying alive in the background. The default is `60`.

The add-on also writes one row per processed PDF to the `logs` worksheet in the configured spreadsheet.

If `mqtt_host` is configured, the add-on publishes a retained heartbeat message to `mqtt_topic` so Home Assistant can detect whether it is online or offline.
