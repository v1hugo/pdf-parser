import tempfile

from flask import Flask, jsonify, request

from parser import main

app = Flask(__name__)


@app.route("/")
def home():
    return "PDF Parser API Running"


@app.route("/process_pdf", methods=["POST"])
def process_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file received"}), 400

    file = request.files["file"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        with open(tmp.name, "rb") as fh:
            result = main(fh, None)

    return jsonify(
        {
            "status": result.get("status", "processed"),
            "validation": result.get("validation", "UNKNOWN"),
            "doc_type": result.get("doc_type", "UNKNOWN"),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
