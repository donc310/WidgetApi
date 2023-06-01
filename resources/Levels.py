from flask import jsonify, request
from flask_restful import Resource
from Model import db, VistorLevel, LevelOptionsSchema, Level2OptionsSchema, Vistor, LocationOptionSchema

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort

level_schema = LevelOptionsSchema
level_schema = LevelOptionsSchema(many=True)

level2_schema = Level2OptionsSchema
level2_schema = Level2OptionsSchema(many=True)

location_schema = LocationOptionSchema
location_schema = location_schema(many=True)


class Level1Resource(Resource):

    queryArgs = {
        "level": fields.Str(),
        "sublevel": fields.Str()
    }
    @use_args(queryArgs)
    def get(self, args):
        if 'sublevel' in args:
            if len(args['sublevel']) != 0:
                location = Vistor.query.filter_by(
                    Level_1=args['level'], Level_2=args['sublevel']).distinct(Vistor.LOCATION).all()
            else:
                location = Vistor.query.filter_by(
                    Level_1=args['level']).distinct(Vistor.LOCATION).all()

            location = location_schema.dump(location).data
            return {"message": "Success", 'data': location}, 200


        elif'level' in args:
            levels = VistorLevel.query.filter_by(
                Level_1=args['level']).distinct(VistorLevel.Level_2).all()
            levels = level2_schema.dump(levels).data
            return {"message": "Success", 'data': levels}, 200

        else:
            levels = VistorLevel.query.distinct(VistorLevel.Level_1).all()
            levels = level_schema.dump(levels).data
            return {"message": "Success", 'data': levels}, 200
