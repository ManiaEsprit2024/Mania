from flask import Blueprint, request, jsonify
from ..auth import verify_token

user_blueprint = Blueprint("users", __name__)

@user_blueprint.route('/me', methods=['GET'])
def get_user_info():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Authorization header is missing"}), 401
    
    token = auth_header.split(" ")[1]
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    return jsonify({"user_id": user_id, "name": "User Name"}), 200
