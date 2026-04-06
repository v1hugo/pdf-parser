#!/bin/sh
set -eu

echo "Starting PDF Parser add-on..."
/opt/venv/bin/python /app/run_drive_parser.py
