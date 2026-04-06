import os
import sys

from parser import main


if len(sys.argv) < 2:
    print("Usage: python run_parser.py <file.pdf>")
    sys.exit(1)

pdf_path = sys.argv[1]
with open(pdf_path, "rb") as fh:
    result = main(fh, f"file://{os.path.abspath(pdf_path)}")

print("Result:")
print(result)
