from flask import Flask, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

# رابط Google Apps Script الخاص فيك
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxh0on2M4HGic5la6SglAh6cW3uVyos9mUn6gp7FvVwoviSkWO2qw0kumXeRYcGOBjlew/exec"

@app.route('/check', methods=['POST'])
def check_subscription():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"status": "error", "message": "email is required"}), 400

    try:
        # نطلب البيانات من Google Sheets
        response = requests.get(GOOGLE_SCRIPT_URL, params={"email": email})

        # اطبع الرد الخام من Google Apps Script
        print("RAW Google Script Response:", response.text)

        # حاول تحوّله JSON
        result = response.json()

        if "error" in result:
            return jsonify({"status": "not_found"}), 404

        expiry = datetime.strptime(result["subscription_until"], "%Y-%m-%d")
        if expiry >= datetime.now():
            return jsonify({"status": "active"}), 200
        else:
            return jsonify({"status": "expired"}), 403

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return "Subscription API Connected to Google Sheets ✅"

# حل مشكلة السيرفر في Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
