from flask import Flask, jsonify
from flask_restx import Api, Resource
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

def get_db(database):
    client = MongoClient('mongodb://mongodb:27017')
    db = client[database]
    return db

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/patients')
class GetPatients(Resource):
    def get(self):
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