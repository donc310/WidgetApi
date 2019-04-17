from flask import jsonify, request
from flask_restful import Resource
from Model import db, VistorLevel , LevelOptionsSchema , Level2OptionsSchema

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort

level_schema = LevelOptionsSchema
level_schema = LevelOptionsSchema(many= True)

level2_schema = Level2OptionsSchema
level2_schema = Level2OptionsSchema(many=True)

class Level1Resource(Resource):
    
    queryArgs={
        "level": fields.Str()
    }
    @use_args(queryArgs)
    def get(self,args):
        if not 'level' in args:
            levels = VistorLevel.query.distinct(VistorLevel.Level_1).all()
            levels = level_schema.dump(levels).data
            return {"message": "Success",'data':levels}, 200
        else:
            levels = VistorLevel.query.filter_by(Level_1=args['level']).distinct(VistorLevel.Level_2).all()
            levels = level2_schema.dump(levels).data
            return {"message": "Success",'data':levels}, 200



            


    

