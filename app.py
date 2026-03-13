
import logging
from flask import Flask, request, jsonify
import tempfile
from parser import main

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@app.route("/")
def home():
    return "PDF Parser API Running"

@app.route("/process_pdf", methods=["POST"])
def process_pdf():
    logging.info("PROCESS_PDF endpoint triggered")

    if 'file' not in request.files:
        return jsonify({"error":"No file received"}), 400

    file = request.files['file']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        result = main(tmp.name)

    return jsonify({
        "status":"processed",
        "validation": result.get("validation","UNKNOWN")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True,use_reloader=False)