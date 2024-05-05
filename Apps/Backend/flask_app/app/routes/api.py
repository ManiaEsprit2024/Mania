from flask import Blueprint, request, jsonify

api = Blueprint('api', __name__)

@api.route('/validate_mania', methods=['POST'])
def validate_mania():
    
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    if username == 'mania' and password == 'mania':
        return jsonify({"message": "OK"}), 200 
    else:
        return jsonify({"error": "Invalid credentials"}), 401