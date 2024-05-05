from flask import Flask
from app.routes.api import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api') 

@app.route('/')
def home():
    return "Welcome to the simple Flask backend!"

if __name__ == '__main__':
    app.run(debug=True)
