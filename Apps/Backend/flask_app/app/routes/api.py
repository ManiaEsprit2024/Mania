from flask import Blueprint, request, jsonify, abort

api = Blueprint('api', __name__)

@api.route('/hello', methods=['GET'])
def say_hello():
    return "Hello from the API!"

@api.route('/echo', methods=['POST'])   
def echo():
    data = request.get_json()
    if not data:
        abort(400, description="No data provided")
    return jsonify(data)

@api.route('/user/<username>', methods=['GET'])
def get_user(username):
    if username == "admin":
        return f"Admin User: {username}"
    else:
        abort(404, description="User not found")