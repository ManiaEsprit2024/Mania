from flask import Flask
from app.routes.api import api
from app.routes.fico import fico

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api') 
app.register_blueprint(fico, url_prefix='/api')

@app.route('/')
def home():
    return "Backend Working"

if __name__ == '__main__':
    app.run(debug=True)