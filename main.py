from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)

# مسار ملف الخدمة من Firebase (لازم تكون حملته من Console)
cred = credentials.Certificate("firebase_service_account.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/check", methods=["POST"])
def check_subscription():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    doc_ref = db.collection("subscriptions").document(email)
    doc = doc_ref.get()

    if doc.exists:
        sub_data = doc.to_dict()
        subscription_until = sub_data.get("subscription_until")

        if subscription_until and subscription_until > datetime.now():
            return jsonify({"status": "active"})
        else:
            return jsonify({"status": "expired"})
    else:
        return jsonify({"status": "not_found"})

if __name__ == "__main__":
    app.run(debug=True)
