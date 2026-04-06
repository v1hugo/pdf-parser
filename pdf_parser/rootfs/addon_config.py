import json
import os
from functools import lru_cache


DEFAULTS = {
    "spreadsheet_id": "",
    "folder_entrada": "",
    "folder_procesados": "",
    "folder_error": "",
    "service_account_path": "/config/pdf_parser/service_account.json",
}


@lru_cache(maxsize=1)
def load_options():
    options = dict(DEFAULTS)
    options_path = "/data/options.json"

    if os.path.exists(options_path):
        with open(options_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            options.update({k: v for k, v in data.items() if v not in (None, "")})

    for key in DEFAULTS:
        env_key = key.upper()
        env_value = os.getenv(env_key)
        if env_value:
            options[key] = env_value

    return options


def get_option(name):
    return load_options().get(name, DEFAULTS.get(name))


def require_option(name):
    value = get_option(name)
    if value in (None, ""):
        raise RuntimeError(f"Missing required add-on option: {name}")
    return value
