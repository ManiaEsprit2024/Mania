from flask import Blueprint, request, jsonify
from ..auth import generate_token, verify_token

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    # Simulated login - in a real-world app, you would authenticate against a database
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Generate a token for the user
    token = generate_token(user_id)
    return jsonify({"token": token}), 200
