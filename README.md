# PDF Parser Home Assistant Add-on Repository

This branch turns `pdf-parser` into a Home Assistant add-on repository that can be added directly from GitHub.

## Install from GitHub

1. In Home Assistant, open `Settings -> Add-ons -> Add-on Store`.
2. Open the menu and choose `Repositories`.
3. Add this repository URL and select branch `ha-addon`:
   `https://github.com/v1hugo/pdf-parser`
4. Install the `PDF Parser` add-on.

## Required add-on options

Set these options before starting the add-on:

- `spreadsheet_id`
- `folder_entrada`
- `folder_procesados`
- `folder_error`
- `service_account_path`

The default credentials path is:

`/config/pdf_parser/service_account.json`

Create that file inside your Home Assistant config directory before running the add-on.
