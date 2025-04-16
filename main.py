from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# بيانات الاشتراكات (مؤقتًا داخل الكود)
users = {
    "test@email.com": {
        "subscription_until": "2025-05-30"
    },
    "expired@email.com": {
        "subscription_until": "2024-12-01"
    }
}

@app.route('/check', methods=['POST'])
def check_subscription():
    data = request.json
    email = data.get("email")
    if email not in users:
        return jsonify({"status": "not_found"}), 404
    
    expiry = datetime.strptime(users[email]["subscription_until"], "%Y-%m-%d")
    if expiry >= datetime.now():
        return jsonify({"status": "active"}), 200
    else:
        return jsonify({"status": "expired"}), 403

@app.route('/')
def home():
    return "Subscription API Running 🚀"

