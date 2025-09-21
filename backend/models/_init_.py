from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS   # Allow frontend to connect

app = Flask(__name__)
CORS(app)   # enable CORS for all routes

# ---------- Database Connection ----------
def get_db():
    conn = sqlite3.connect("jobs.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- USERS ----------
@app.route("/users", methods=["POST"])
def register_user():
    data = request.json
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (data["username"], data["email"], data["password"]))
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/users/login", methods=["POST"])
def login_user():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (data["username"], data["password"]))
    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }), 200
    return jsonify({"error": "Invalid credentials"}), 401


# ---------- HELP REQUESTS ----------
@app.route("/requests", methods=["POST"])
def create_request():
    data = request.json
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO help_requests (title, description, user_id) VALUES (?, ?, ?)",
                    (data["title"], data["description"], data["user_id"]))
        conn.commit()
        conn.close()
        return jsonify({"message": "Help request created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/requests", methods=["GET"])
def get_requests():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""SELECT hr.id, hr.title, hr.description, u.username 
                   FROM help_requests hr 
                   JOIN users u ON hr.user_id=u.id""")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


# ---------- JOBS ----------
@app.route("/jobs", methods=["POST"])
def create_job():
    data = request.json
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO jobs (title, company, location, description) VALUES (?, ?, ?, ?)",
                    (data["title"], data["company"], data["location"], data["description"]))
        conn.commit()
        conn.close()
        return jsonify({"message": "Job posted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/jobs", methods=["GET"])
def get_jobs():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in jobs])


# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(debug=True)
