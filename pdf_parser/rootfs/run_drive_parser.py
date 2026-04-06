import time

from addon_config import get_int_option
from parser import main
from utils.drive import (
    FOLDER_ENTRADA,
    FOLDER_ERROR,
    FOLDER_PROCESADOS,
    download_file_to_memory,
    get_file_url,
    list_pdfs,
    move_file,
)


def process_drive_pdfs():
    files = list_pdfs(FOLDER_ENTRADA)
    print(f"Files found: {len(files)}")

    for file in files:
        file_id = file["id"]
        file_name = file["name"]

        print(f"Processing: {file_name}")

        try:
            file_stream = download_file_to_memory(file_id)
            file_url = get_file_url(file_id)
            result = main(file_stream, file_url)
            seleccion_id = result.get("seleccion_id")

            if result.get("validation") == "OK":
                move_file(file_id, FOLDER_PROCESADOS, seleccion_id)
                print("Moved file to processed folder.")
            else:
                move_file(file_id, FOLDER_ERROR)
                print("Moved file to error folder due to failed validation.")
        except Exception as exc:
            print(f"Error processing {file_name}: {exc}")
            move_file(file_id, FOLDER_ERROR)


def run_forever():
    poll_interval_seconds = get_int_option("poll_interval_seconds", minimum=5)
    print(
        f"PDF Parser add-on started. Polling Google Drive every {poll_interval_seconds} seconds."
    )

    while True:
        cycle_started_at = time.time()

        try:
            process_drive_pdfs()
        except Exception as exc:
            print(f"Drive polling cycle failed: {exc}")

        elapsed = time.time() - cycle_started_at
        sleep_seconds = max(poll_interval_seconds - elapsed, 1)
        print(f"Sleeping for {int(sleep_seconds)} seconds.")
        time.sleep(sleep_seconds)


if __name__ == "__main__":
    run_forever()
