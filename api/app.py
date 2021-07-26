from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)


### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###



def get_db():
    client = MongoClient('mongodb://mongodb:27017')
    db = client["food"]
    return db

@app.route('/')
def ping_server():
    return "Welcome to the world of animals."

@app.route('/food')
def get_stored_food():
    db = get_db()
    _fruits = db.fruits.find()
    fruits = [{
    "name": fruit["name"], 
    "origin": fruit["origin"], 
    "price": fruit["price"]
    } for fruit in _fruits]
    return jsonify({"fruits": fruits})

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)