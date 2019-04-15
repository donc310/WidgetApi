from flask import jsonify, request
from flask_restful import Resource
from Model import db, VistorLevel, VistorLevelSchema

schema_level = VistorLevelSchema
schema_level = VistorLevelSchema(many=True)


class ChainResource(Resource):
    def get(self):
        level = VistorLevel.query.all()
        level = schema_level.dump(level).data
        return {"status": "success", "data": level}, 200
    
