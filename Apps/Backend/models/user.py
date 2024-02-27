from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo

class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def save(self):
        users = mongo.db.users
        users.insert_one({'username': self.username, 'password_hash': self.password_hash})

    @staticmethod
    def find_by_username(username):
        users = mongo.db.users
        user_data = users.find_one({'username': username})
        if user_data:
            return User(user_data['username'], user_data['password_hash'])
        return None
