from flask import Flask, request, jsonify
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/', methods=['POST'])
def check_subscription():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    doc_ref = db.collection("subscriptions").document(email)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({"valid": False})

    subscription_data = doc.to_dict()
    subscription_until = subscription_data.get("subscription_until")

    if not subscription_until:
        return jsonify({"valid": False})

    now = datetime.utcnow()
    if subscription_until > now:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})

if __name__ == '__main__':
    app.run()
