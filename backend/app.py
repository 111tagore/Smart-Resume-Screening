# app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import uuid
from db import get_db_connection
from utils import extract_text, clean_text, extract_keywords_from_jobrole
from ml_engine import compute_scores

load_dotenv()
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, supports_credentials=True)

def insert_user(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO users (first_name,last_name,employee_role,employee_id,department,email,password)
             VALUES (%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql, (
        user['first_name'], user['last_name'], user['employee_role'], user['employee_id'],
        user['department'], user['email'], user['password']
    ))
    conn.commit()
    uid = cursor.lastrowid
    cursor.close()
    conn.close()
    return uid

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def save_resume_record(filename, filepath, extracted_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO resumes (filename, filepath, text_content) VALUES (%s,%s,%s)"""
    cursor.execute(sql, (filename, filepath, extracted_text))
    conn.commit()
    rid = cursor.lastrowid
    cursor.close()
    conn.close()
    return rid

def save_result_record(resume_id, score, analysis_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO results (resume_id, score, analysis_id) VALUES (%s,%s,%s)"
    cursor.execute(sql, (resume_id, score, analysis_id))
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    required = ['first_name','last_name','employee_role','employee_id','department','email','password']
    if not all(k in data for k in required):
        return jsonify({"success":False,"message":"Missing fields"}),400
    if get_user_by_email(data['email']):
        return jsonify({"success":False,"message":"User already exists"}),400
    uid = insert_user(data)
    return jsonify({"success":True,"message":"User registered","user_id": uid})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if 'email' not in data or 'password' not in data:
        return jsonify({"success":False,"message":"missing fields"}),400
    user = get_user_by_email(data['email'])
    if not user or user['password'] != data['password']:
        return jsonify({"success":False,"message":"invalid credentials"}),401
    user_safe = {k:v for k,v in user.items() if k!='password'}
    return jsonify({"success":True,"user":user_safe})

@app.route("/upload_resumes", methods=["POST"])
def upload_resumes():
    if 'files' not in request.files:
        return jsonify({"success":False,"message":"No files uploaded"}),400
    files = request.files.getlist("files")
    saved = []
    for f in files:
        filename = f.filename
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        f.save(file_path)
        try:
            extracted = extract_text(file_path, filename)
            cleaned = clean_text(extracted)
            rid = save_resume_record(filename, file_path, cleaned)
            saved.append({"resume_id":rid, "filename": filename})
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            print("Extraction error:", e)
    return jsonify({"success":True, "saved": saved})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    job_role = data.get("job_role","")
    openings = int(data.get("openings",1))
    if not job_role:
        return jsonify({"success":False,"message":"job_role required"}),400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, filename, filepath, text_content FROM resumes")
    resumes = cursor.fetchall()
    cursor.close()
    conn.close()
    resume_texts = [r['text_content'] for r in resumes]
    cleaned_job = clean_text(job_role)
    keywords = extract_keywords_from_jobrole(job_role, top_k=10)
    scores = compute_scores(resume_texts, cleaned_job)
    combined = []
    for r,s in zip(resumes, scores):
        combined.append({"resume_id": r['id'], "filename": r['filename'],
                         "score": s, "filepath": r['filepath']})
    combined_sorted = sorted(combined, key=lambda x: x['score'], reverse=True)
    top_selected = combined_sorted[:openings]
    analysis_id = uuid.uuid4().hex
    for item in combined_sorted:
        save_result_record(item['resume_id'], item['score'], analysis_id)

    return jsonify({
        "success":True,
        "analysis_id": analysis_id,
        "keywords": keywords,
        "ranked_results": combined_sorted,
        "selected": top_selected
    })

@app.route("/get_results/<analysis_id>", methods=["GET"])
def get_results(analysis_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT r.id as result_id, r.resume_id, r.score, r.analysis_id, re.filename
             FROM results r
             JOIN resumes re ON re.id = r.resume_id
             WHERE r.analysis_id = %s
             ORDER BY r.score DESC"""
    cursor.execute(sql, (analysis_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success":True, "results": rows})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
