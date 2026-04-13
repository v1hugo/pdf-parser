ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-pip

WORKDIR /app

COPY rootfs/ /app/

RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

CMD ["/opt/venv/bin/python", "/app/run_drive_parser.py"]
