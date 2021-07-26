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



def get_db(database):
    client = MongoClient('mongodb://mongodb:27017')
    db = client[database]
    return db

@app.route('/')
def ping_server():
    return "Welcome to the world of animals."

@app.route('/patients')
def get_patients_info():
    db = get_db("patients")
    _patients = db.patients.find()
    patients = [{
        "name":patient["name"],
        "dob":patient["dob"],
        "sex":patient["sex"]
    } for patient in _patients]
    return jsonify({"patients": patients})

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)