from flask import Flask
from flask_cors import CORS
from app.routes.api import api
from app.routes.fico import fico

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})  # Allow requests from your Angular app's URL

app.register_blueprint(api, url_prefix='/api') 
app.register_blueprint(fico, url_prefix='/api')

@app.route('/')
def home():
    return "Backend Working"

if __name__ == '__main__':
    app.run(debug=True)
