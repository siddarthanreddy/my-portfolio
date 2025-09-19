from flask import Flask, render_template, request, jsonify
from datetime import datetime
import csv
import os

# Initialize Flask
app = Flask(__name__, static_folder="static", template_folder="templates")

# File to store contact messages
MESSAGES_FILE = "messages.csv"

# Ensure messages file exists with a header
if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "name", "email", "message"])


# ---------------- Routes ---------------- #

# Home route
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Contact form submission (AJAX)
@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    timestamp = datetime.utcnow().isoformat()

    # Save the message to CSV
    with open(MESSAGES_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, name, email, message])

    return jsonify({"status": "ok", "message": "Thanks! I received your message."})


# ---------------- Main Entry ---------------- #
if __name__ == "__main__":
    # For local development and Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
