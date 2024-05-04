from flask import Flask
from .config import Config
from .routes.auth_routes import auth_blueprint
from .routes.user_routes import user_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/users')

    return app
