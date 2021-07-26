from flask import Flask, jsonify, request
from flask_restx import Api, Resource
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app, version='1.0', title='Electronic Health Records',
    description='A simple api for EHR')

ns = api.namespace('EHR', description='Electronic Health Records')

def get_db(database):
    client = MongoClient('mongodb://mongodb:27017')
    db = client[database]
    return db

@ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@ns.route('/patients')
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


@ns.route('/patient/<int:id>')
class GetPatients(Resource):
    def get(self, id):
        db = get_db("patients")
        _patients = db.patients.find()
        patients = [{
            "name":patient["name"],
            "dob":patient["dob"],
            "sex":patient["sex"]
        } for patient in _patients]
        return jsonify({"patients": patients[id]})



if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)