from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.user import User
import time
import app.models
import secrets
from app.config.database import Database

app = Flask(__name__)

new_secret_key = secrets.token_hex(32)
app.config['JWT_SECRET_KEY'] = new_secret_key
jwt = JWTManager(app)

db = Database()

@app.route('/api/user/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    try:
        response, status_code = User.register_user(username, password)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/user/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    try:
        mongo = db.get_db()
        response, status_code = User.login_user(username, password, mongo)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/')
def home():
    return "Hello World"
    
if __name__ == '__main__':
    # Print ASCII art animation
    print("""
  __  __  _____          __  __          _   _ _____          
 |  \/  |/ ____|   _    |  \/  |   /\   | \ | |_   _|   /\    
 | \  / | |       (_)   | \  / |  /  \  |  \| | | |    /  \   
 | |\/| | |             | |\/| | / /\ \ | . ` | | |   / /\ \  
 | |  | | |____    _    | |  | |/ ____ \| |\  |_| |_ / ____ \ 
 |_|  |_|\_____|  (_)   |_|  |_/_/    \_\_| \_|_____/_/    \_\
""")

    print("                                                       ")
    print("MC BackEnd Server is running on http://127.0.0.1:5000\n")
    time.sleep(1)
    app.run(debug=True,port=5000)