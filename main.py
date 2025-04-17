from flask import Flask, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxh0on2M4HGic5la6SglAh6cW3uVyos9mUn6gp7FvVwoviSkWO2qw0kumXeRYcGOBjlew/exec"

@app.route('/check', methods=['POST'])
def check_subscription():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"status": "error", "message": "email is required"}), 400

    try:
        response = requests.get(GOOGLE_SCRIPT_URL, params={"email": email})

        # ✅ اطبع الرد الكامل من Google Script
        print("RAW Google Script Response:", response.text, flush=True)

        result = response.json()

        if "error" in result:
            return jsonify({"status": "not_found"}), 404

        expiry = datetime.strptime(result["subscription_until"], "%Y-%m-%d")
        if expiry >= datetime.now():
            return jsonify({"status": "active"}), 200
        else:
            return jsonify({"status": "expired"}), 403

    except Exception as e:
        print("🔥 ERROR:", str(e), flush=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return "Subscription API Connected to Google Sheets ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
