from flask import jsonify, request
from flask_restful import Resource
from Model import db, States ,StatesSchema

schema_states = StatesSchema()
schema_states = StatesSchema(many=True)

class StatesResource(Resource):
    def get(self):
        states = States.query.all()
        states = schema_states.dump(states).data
        return {"status":"success", "data":states}, 200
    
