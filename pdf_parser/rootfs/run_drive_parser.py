import json
import signal
import time

import paho.mqtt.client as mqtt

from addon_config import get_int_option, get_option
from parser import main
from sheets import append_process_log
from utils.drive import (
    FOLDER_ENTRADA,
    FOLDER_ERROR,
    FOLDER_PROCESADOS,
    download_file_to_memory,
    get_file_url,
    list_pdfs,
    move_file,
)


class HeartbeatPublisher:
    def __init__(self):
        self.client = None
        self.topic = get_option("mqtt_topic") or "pdf_parser/status"
        self.enabled = bool(get_option("mqtt_host"))

        if not self.enabled:
            return

        try:
            self.client = mqtt.Client()

            username = get_option("mqtt_username")
            password = get_option("mqtt_password")
            if username:
                self.client.username_pw_set(username, password or None)

            offline_payload = json.dumps({"status": "offline"})
            self.client.will_set(self.topic, offline_payload, qos=1, retain=True)

            host = get_option("mqtt_host")
            port = get_int_option("mqtt_port", minimum=1)
            self.client.connect(host, port, keepalive=60)
            self.client.loop_start()
        except Exception as exc:
            print(f"MQTT heartbeat disabled: {exc}")
            self.client = None

    def publish(self, status):
        if not self.client:
            return

        payload = json.dumps(
            {
                "status": status,
                "timestamp": int(time.time()),
            }
        )
        self.client.publish(self.topic, payload, qos=1, retain=True)

    def close(self):
        if not self.client:
            return

        try:
            self.publish("offline")
            self.client.loop_stop()
            self.client.disconnect()
        finally:
            self.client = None


def process_drive_pdfs():
    files = list_pdfs(FOLDER_ENTRADA)
    print(f"Files found: {len(files)}")

    for file in files:
        file_id = file["id"]
        file_name = file["name"]
        file_url = get_file_url(file_id)
        result = None
        error = None

        print(f"Processing: {file_name}")

        try:
            file_stream = download_file_to_memory(file_id)
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
            error = exc
            try:
                move_file(file_id, FOLDER_ERROR)
            except Exception as move_exc:
                print(f"Error moving {file_name} to error folder: {move_exc}")
                error = RuntimeError(f"{exc}; move_file failed: {move_exc}")
        finally:
            try:
                append_process_log(file_name, file_id, file_url, result=result, error=error)
            except Exception as log_exc:
                print(f"Error writing log for {file_name}: {log_exc}")


def run_forever():
    poll_interval_seconds = get_int_option("poll_interval_seconds", minimum=5)
    heartbeat = HeartbeatPublisher()

    def handle_shutdown(signum, frame):
        del signum
        del frame
        heartbeat.close()
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    print(
        f"PDF Parser add-on started. Polling Google Drive every {poll_interval_seconds} seconds."
    )

    try:
        while True:
            cycle_started_at = time.time()
            heartbeat.publish("online")

            try:
                process_drive_pdfs()
            except Exception as exc:
                print(f"Drive polling cycle failed: {exc}")

            elapsed = time.time() - cycle_started_at
            sleep_seconds = max(poll_interval_seconds - elapsed, 1)
            print(f"Sleeping for {int(sleep_seconds)} seconds.")
            time.sleep(sleep_seconds)
    finally:
        heartbeat.close()


if __name__ == "__main__":
    run_forever()
