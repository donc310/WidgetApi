from flask import jsonify, request
from flask_restful import Resource
from Model import db, States ,StatesSchema , VisitorAudienceTotal,VistorLevelSchema ,VistorChainsTotal , Names
from webargs.flaskparser import use_args, use_kwargs, parser, abort
from webargs import fields, validate

schema_states = StatesSchema()
schema_states = StatesSchema(many=True)


audienceTotal = VisitorAudienceTotal
audienceTotal = VisitorAudienceTotal(many=True)


stateNames = Names
stateNames=Names(many=True)

class StatesResource(Resource):
    def get(self):
        states = States.query.all()
        states = stateNames.dump(states).data
        return {"status":"success", "data":states}, 200

    def getwe(self):
        states = States.query.all()
        states = schema_states.dump(states).data
        for x in states:
            query = self._search(x['abv'])
            x['AudienceTotal'] = f"{x['name']} : Estimated {query}"

        return {"status":"success", "data":states}, 200
    def _search(self,statecode):
        _query = VistorChainsTotal.query.filter_by(state=statecode).all()
        _query = audienceTotal.dump(_query).data
        total = 0
        if len(_query) != 0:
            for index in range(len(_query)):
                total += _query[index]['AudienceTotal']
        return total      
    queryArgs={
        'like':fields.Str()
    }
    @use_args(queryArgs)
    def me(self, arg):
        if 'like' not in arg:
            return {"status":"success", "data":[]}, 200
        states = States.query.all()
        states = schema_states.dump(states).data
        LIMIT = 10
        RES = [x for x in states if x['name'].find(arg['like'].capitalize()) is not -1]
        return {"status":"success", "data":RES}, 200
    
