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
    print("Starting PDF processing from Google Drive...")

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


if __name__ == "__main__":
    process_drive_pdfs()
