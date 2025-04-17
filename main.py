import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify

# Initialize Firebase
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

app = Flask(__name__)

@app.route('/check', methods=['POST'])
def check_subscription():
    data = request.get_json()
    email = data.get('email')

    # Fetch the user document from Firestore
    users_ref = db.collection('subscriptions')
    user_doc = users_ref.document(email).get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        subscription_until = user_data.get('subscription_until')
        if subscription_until:
            return jsonify({"status": "success", "subscription_until": subscription_until})
        else:
            return jsonify({"status": "error", "message": "No subscription date found"})
    else:
        return jsonify({"status": "error", "message": "Email not found"})

if __name__ == '__main__':
    app.run(debug=True)
