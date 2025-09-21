from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder="../frontend")
CORS(app)  # allow frontend JS requests

# --- Database helper ---
def get_db_connection():
    conn = sqlite3.connect("jobs.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- Initialize DB (run once automatically) ---
def init_db():
    if not os.path.exists("jobs.db"):
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("✅ Database created: jobs.db")

init_db()

# --- API Routes ---
@app.route("/jobs", methods=["GET"])
def get_jobs():
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    conn.close()
    return jsonify([dict(job) for job in jobs])

@app.route("/jobs", methods=["POST"])
def add_job():
    new_job = request.get_json()
    title = new_job["title"]
    company = new_job["company"]
    location = new_job["location"]
    description = new_job["description"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO jobs (title, company, location, description) VALUES (?, ?, ?, ?)",
        (title, company, location, description),
    )
    conn.commit()
    conn.close()

    return jsonify(new_job), 201

# --- Serve Frontend ---
@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:filename>")
def frontend(filename):
    return send_from_directory("../frontend", filename)

if __name__ == "__main__":
    app.run(debug=True)
