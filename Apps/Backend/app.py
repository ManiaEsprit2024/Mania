from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import time

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/user_db'
mongo = PyMongo(app)

@app.route('/api/register', methods=['POST'])
def register():
    users = mongo.db.users
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if users.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400

    password_hash = generate_password_hash(password)
    new_user = {'username': username, 'password_hash': password_hash}
    users.insert_one(new_user)

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    users = mongo.db.users
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.find_one({'username': username})

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful'}), 200

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