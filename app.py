from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Category import CategoryResource
from resources.Comment import CommentResource
from resources.States import StatesResource
from resources.Data import DataResource
from resources.Total import TotalResource ,GetState
from resources.Chain import ChainResource
from resources.Levels import Level1Resource
from resources.Query import QueryResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(Hello, '/Hello')
api.add_resource(CategoryResource, '/Category')
api.add_resource(CommentResource, '/Comment')
api.add_resource(StatesResource,'/states')
api.add_resource(DataResource,'/data')
api.add_resource(TotalResource,'/totals')
api.add_resource(GetState,'/getstate')
api.add_resource(ChainResource, '/chains')
api.add_resource(Level1Resource,'/leveloptions')
api.add_resource(QueryResource,'/stats/query')