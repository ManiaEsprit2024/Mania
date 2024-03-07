from werkzeug.security import generate_password_hash, check_password_hash
from app.config.database import Database

class User:
    db = Database()

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def save(self):
        users = User.db.get_db().users
        users.insert_one({'username': self.username, 'password_hash': self.password_hash})

    @staticmethod
    def register_user(username, password):
        password_hash = generate_password_hash(password)
        user = User(username, password_hash)
        user.save()
        return {'message': 'User registered successfully'}, 201

    @staticmethod
    def find_by_username(username):
        users_collection = User.db.get_db().users
        user_data = users_collection.find_one({'username': username})
        if user_data:
            return User(user_data['username'], user_data['password_hash'])
        else:
            return None


    @staticmethod
    def login_user(username, password):
        user = User.find_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            return {'message': 'Login successful'}, 200
        else:
            return {'message': 'Invalid username or password'}, 401
