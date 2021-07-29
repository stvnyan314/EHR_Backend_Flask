from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
import pymongo
from pymongo import MongoClient

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

@ns.route('/patients')
class GetPatients(Resource):
    def get(self):
        db = get_db("patients")
        _patients = db.patients.find({},{ "_id": 0})
        patients = [patient for patient in _patients]
        return jsonify({"patients": patients})


@ns.route('/patient/<int:id>')
class GetPatients(Resource):
    def get(self, id):
        db = get_db("patients")
        _patients = db.patients.find({},{ "_id": 0})
        patients = [patient for patient in _patients]
        return jsonify({"patients": patients[id]})

@ns.route('/newpatient')
@ns.expect(patient_model)
class AddPatient(Resource):
    def post(self):
        db = get_db("patients")
        db.patients.insert_one(request.json)
        return {"status": db.patients.count()}

@ns.route('/findpatient')
@ns.expect(patient_model)
class FindPatients(Resource):
    def put(self):
        db = get_db("patients")
        patient_query = request.json
        _patients = db.patient.find(patient_query)
        patients = [patient for patient in _patients]
        print(patient_query)
        return {"matching patient": patients}


if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)