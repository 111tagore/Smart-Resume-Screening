# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Import your modules correctly
from services.resume_parser import parse_resume
from services.ml_engine import rank_resumes

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------
# 1️⃣ Upload + Parse Resume
# ---------------------------
@app.route("/parse", methods=["POST"])
def parse_route():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    parsed = parse_resume(file_path)
    return jsonify(parsed), 200


# ---------------------------
# 2️⃣ Rank multiple resumes
# ---------------------------
@app.route("/rank", methods=["POST"])
def rank_route():
    data = request.json

    resume_texts = data.get("resumes")
    job_description = data.get("job_description")
    file_names = data.get("file_names", None)
    top_n = data.get("top_n", None)

    if not resume_texts or not job_description:
        return jsonify({"error": "Missing resume texts or job description"}), 400

    results = rank_resumes(
        resume_texts=resume_texts,
        job_description=job_description,
        file_names=file_names,
        top_n=top_n
    )

    return jsonify(results), 200


@app.route("/", methods=["GET"])
def home():
    return {"message": "Smart Resume Screening API is running!"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
