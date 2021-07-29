from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
import pymongo
from pymongo import MongoClient
import json
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app, version='1.0', title='Electronic Health Records',
    description='A simple api for EHR')

ns = api.namespace('EHR', description='Electronic Health Records')

patient_model = ns.model('Patient Model', 
                {
                    'first_name': fields.String(required = False,
                        example = "John",
                        description="First name of the person", 
                        help="Name cannot be blank."),
                    'middle_name': fields.String(required = False, 
                        description="First name of the person"),
                    'last_name': fields.String(required = False, 
                        example = "Doe",
                        description="Last name of the person", 
                        help="Name cannot be blank."),
                    'dob': fields.String(required = False,
                        description="Date of birth",
                        help="DOB cannot be blank."),
                    'sex': fields.String(required = False,
                        description="Sex of person")
                })

def get_db(database):
    client = MongoClient('mongodb://mongodb:27017')
    db = client[database]
    return db

def get_collection(database, collection):
    client = MongoClient('mongodb://mongodb:27017')
    db = client[database]
    coll = db.get_collection(collection)
    return coll

def parse_json(data):
    return json.loads(dumps(data))

@ns.route('/patients')
class GetPatients(Resource):
    def get(self):
        coll = get_collection("patients", "patients")
        _patients = coll.find({})
        patients = [parse_json(patient) for patient in _patients]
        return jsonify({"patients": patients})


@ns.route('/patient/<int:id>')
class GetPatients(Resource):
    def get(self, id):
        coll = get_collection("patients", "patients")
        _patients = coll.find({})
        patients = [parse_json(patient) for patient in _patients]
        return jsonify({"patients": patients[id]})

@ns.route('/newpatient')
@ns.expect(patient_model)
class AddPatient(Resource):
    def post(self):
        coll = get_collection("patients", "patients")
        coll.insert_one(request.json)
        return {"status": coll.count()}

@ns.route('/findpatient')
@ns.expect(patient_model)
class FindPatients(Resource):
    def put(self):
        patient_query = request.json
        coll = get_collection("patients", "patients")
        _patients = coll.find(patient_query)
        patients = [parse_json(patient) for patient in _patients]
        return jsonify({"patients": patients})

@ns.route('/deletepatient/<oid>')
class DeletePatients(Resource):
    def put(self, oid):
        patient_delete = {"_id": ObjectId(oid)}
        coll = get_collection("patients", "patients")
        status = coll.delete_one(patient_delete)
        return {"status": parse_json(status)}

@ns.route('/updatepatient/<oid>')
@ns.expect(patient_model)
class UpdatePatients(Resource):
    def put(self, oid):
        patient_update = request.json
        patient_update.append({"_id": {"$oid": oid}})
        #coll = get_collection("patients", "patients")
        #_patients = coll.update_one({"_id": {"$oid": oid}})
        #patients = [parse_json(patient) for patient in _patients]
        return jsonify({"patients": patient_update})


if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)