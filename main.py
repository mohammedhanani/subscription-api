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
        # نطلب كل البيانات من Google Sheets
        response = requests.get(GOOGLE_SCRIPT_URL)
        sheet_data = response.json()

        for entry in sheet_data:
            if entry.get("email", "").lower() == email.lower():
                expiry_str = entry.get("subscription_until", "")
                try:
                    expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
                    if expiry >= datetime.now():
                        return jsonify({"status": "active"}), 200
                    else:
                        return jsonify({"status": "expired"}), 403
                except:
                    return jsonify({"status": "error", "message": "Invalid date format"}), 500

        return jsonify({"status": "not_found"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return "Subscription API Connected to Google Sheets ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
