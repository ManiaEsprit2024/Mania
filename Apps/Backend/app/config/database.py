from flask_pymongo import PyMongo

class Database:
    uri = "mongodb://localhost:27017/mania"

    def __init__(self, app=None):
        self.init_app(app)

    def init_app(self, app):
        if self.uri is None:
            raise ValueError("URI and dbname must be provided.")
        self.mongo = PyMongo(app, uri=self.uri)

    def get_db(self):
        if not hasattr(self, 'mongo'):
            raise Exception('Database connection has not been initialized. Call init_app() first.')
        return self.mongo.db
