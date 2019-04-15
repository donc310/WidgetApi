from flask import jsonify, request
from flask_restful import Resource
from Model import db, VistorChainsTotal, VisitorChainTotalSchma , VistorLevel, VistorLevelSchema , VisitorAudienceTotal

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort

schema_total = VisitorChainTotalSchma
schema_total = VisitorChainTotalSchma(many=True)

audienceTotal = VisitorAudienceTotal
audienceTotal = VisitorAudienceTotal(many=True)


class TotalResource(Resource):
    def get(self):
        total = VistorChainsTotal.query.all()
        total = schema_total.dump(total).data
        return {"status": "success", "data": total}, 200


class GetState(Resource):

    queryArgs = {
        "statecode": fields.Str(),
        "mapIndex": fields.Integer(),
        "query":fields.DelimitedList(fields.Str(), delimiter=',' ),
    }
    @use_args(queryArgs)
    def get(self, args):
        queries=[]
        if not "statecode" in args:
            return {"Error": "Missing State in query"}, 400

        if not "mapIndex" in args:
            return {"Error": "Missing MapIndex in query "}, 400
        
        if 'query' in args:
            search_query = args['query']
        else:
            search_query = []
        
        query = self._search(args['statecode'],args['mapIndex'],search_query)
        
        data = {
           'estimated' : query,
           'Query':{
               'count':len(search_query),
                'filter':search_query
           },
           'state':args['statecode'],
           'mapIndex':args['mapIndex']
        }
        return {"message": "Success",'data':data}, 200
    
    
    def _search(self,statecode,mapIndex, querys):
        _query = VistorChainsTotal.query.filter_by(state=statecode).all()
        _query = audienceTotal.dump(_query).data
        total = 0 
        if not len(_query) == 0:
            index = 0 
            while index < len(_query):
                total += _query[index]['AudienceTotal']
                index += 1
            return total
        else:
            return total
        


@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)
