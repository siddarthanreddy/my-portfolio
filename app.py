from flask import Flask, render_template, request, jsonify
from datetime import datetime
import csv
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

MESSAGES_FILE = "messages.csv"

# Ensure messages file exists with header
if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "name", "email", "message"])

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    timestamp = datetime.utcnow().isoformat()
    # Save to CSV
    with open(MESSAGES_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, name, email, message])

    # (Optional) Could send email here using SMTP or a transactional API.
    return jsonify({"status": "ok", "message": "Thanks! I received your message."})

if __name__ == "__main__":
    app.run(debug=True)
