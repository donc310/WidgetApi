from flask import jsonify, request
from flask_restful import Resource
from Model import db, Vistor ,VisitorSchema

schema_data = VisitorSchema()
schema_data = VisitorSchema(many=True)

class DataResource(Resource):
    def get(self):
        data  = Vistor.query.all()
        data = schema_data.dump(data).data
        return {"status":"success", "data":data}, 200
    
