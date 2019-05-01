from flask import jsonify, request
from flask_restful import Resource

from Model import db, VistorChainsTotal, VistorLevel, Vistor, States

from Model import VisitorChainTotalSchema, VistorLevelSchema, VisitorSchema, QuerySchema, StatesSchema, Names

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort

from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy import Column, Date, Integer, Text, create_engine, inspect, and_, or_
import datetime

currentDT = datetime.datetime.now()

visitor_chain_schema = VisitorChainTotalSchema
visitor_chain_schema = VisitorChainTotalSchema(many=True)

visitor_schema = VisitorSchema
visitor_schema = VisitorSchema(many=True)

visitor_level_schema = VistorLevelSchema
visitor_level_schema = VistorLevelSchema(many=True)

query_schema = QuerySchema
query_schema = QuerySchema(many=True)

schema_states = StatesSchema()
schema_states = StatesSchema(many=True)


class QueryResource(Resource):
	queryArgs = {
		"Level_1": fields.Str(),
		"Level_2": fields.Str(),
		"name": fields.Str(),
		"location": fields.Str(),
		"audience": fields.Str(),
		"frequency": fields.List(fields.Str()),
		"states": fields.List(fields.Str())
	}

	def _get(self, code):
		states = States.query.filter_by(abv=code).all()
		states = schema_states.dump(states).data
		return states

	def anayzedata(self, response):
		for x in response:
			y = x['ID']
			q = x['state']
			count = 0
			for z in response:
				if z['ID'] == y and z['state'] == q:
					count += 1
			x['count'] = count
		return response

	@use_args(queryArgs)
	def get(self, args):
		name = ""
		Level_1 = ""
		Level_2 = ""
		if 'name'in args:
			name = args['name']
		if 'Level_1'in args:
			level_1 = args['Level_1']
		if 'Level_2'in args:
			level_2 = args['Level_2']

		if 'location' in args and not args['location'] == "":
			res = Vistor.query.filter_by(LOCATION=args['location']).all()
			result = visitor_schema.dump(res).data
		elif 'Level_2' in args and not args['Level_2'] == "":
			res = Vistor.query.filter_by(Level_2=args['Level_2']).all()
			result = visitor_schema.dump(res).data

		elif 'Level_1' in args and not args['Level_1'] == "":
			res = Vistor.query.filter_by(Level_1=args['Level_1']).all()
			result = visitor_schema.dump(res).data
		else:
			res = Vistor.query.all()
			result = visitor_schema.dump(res).data

		audience = ""
		frequency = []
		states = []
		_response = []
		if 'audience' in args:
			audience = args['audience']
		if 'states' in args:
			states = args['states']
		if 'frequency' in args:
			frequency = args['frequency']
		if audience == 'states' and len(states) >= 1 and len(res) >= 1:
			for index, _rep in enumerate(result):
				if _rep['state'] in states:
					_response.append(_rep)
		else:
			_response = result
		if len(frequency) >= 1:
			frequencyMap = self.parseFrequency(frequency)
			if frequencyMap:
				if frequencyMap == [1, 0, 0]:
					_response = [i for i in _response if (i['Mild'] == 1)]
				elif frequencyMap == [0, 1, 0]:
					_response = [i for i in _response if (i['Moderate'] == 1)]
				elif frequencyMap == [0, 0, 1]:
					_response = [i for i in _response if (i['Frequent'] == 1)]
				elif frequencyMap == [1, 1, 0]:
					_response = [i for i in _response if (
						i['Mild'] == 1 and i['Moderate'] == 1)]
				elif frequencyMap == [1, 0, 1]:
					_response = [i for i in _response if (
						i['Mild'] == 1 and i['Frequent'] == 1)]
				elif frequencyMap == [0, 1, 1]:
					_response = [i for i in _response if (
						i['Moderate'] == 1 and i['Frequent'] == 1)]
		if len(_response) >= 1:
			for x, y in enumerate(_response):
				y['_map'] = self._get(y['state'])

		ananyzlized = self.anayzedata(_response)
		l_frengency = [i for i in range(0, len(frequency))]
		metadata = {
			'queryname': name,
			'queries': {
				'audience': audience,
				'Level_1': Level_1,
				'Level_2': Level_2,
				'frequecy': dict(zip(l_frengency, frequency)),
				'states': dict(zip([i for i in range(0, len(states))], states))
			},
			'time': str(datetime.datetime.now().timestamp())
		}
		return {"message": "Success", 'data': ananyzlized, 'meta': metadata}, 200

	@use_args(queryArgs)
	def get1(self, args):
		# _query = self.parseQuery(args)

		total = Vistor.query
		_level_1 = None
		_level_2 = None

		if not args["Level_1"] == "":
			_level_1 = args['Level_1']

		if not args['Level_2'] == "":
			_level_2 = args['Level_2']

		if type(_level_1) == str and type(_level_2) == str:
			total = total.filter_by(Level_1=_level_1, Level_2=_level_2)

		else:
			if type(_level_1) == str:
				total = total.filter_by(Level_1=_level_1)
			if type(_level_2) == str:
				total = total.filter_by(Level_2=_level_2)

		if 'location' in args and not args['location'] == "":
			_location = args['location']
			total = total.filter_by(LOCATION=_location)

		if 'frequency' in args:
			if(len(args['frequency'])) == 3:
				total = total.filter(
					or_(Vistor.Frequent == 1, Vistor.Mild == 1, Vistor.Moderate == 1))
			elif 'Frequent' in args['frequency']:
				total = total.filter_by(Frequent=1)
			elif 'Moderate' in args['frequency']:
				total = total.filter_by(Moderate=1)
			elif 'Mild' in args['frequency']:
				total = total.filter_by(Mild=1)
		if "states" in args and args['audience'] == "states":
			if len(args['states']) >= 1:
				pass
				# total = total.filter(and_(Vistor.state.in_([args['states']])))

	def parseFrequency(self, frequency):
		if len(frequency) == 3:
			return False
		elif 'Frequent' in frequency:
			_frequent = 1
		elif not 'Frequent' in frequency:
			_frequent = 0
		elif 'Moderate' in frequency:
			_moderate = 1
		elif not 'Moderate' in frequency:
			_moderate = 0
		elif 'Mild' in frequency:
			_mild = 1
		elif not 'Mild' in frequency:
			_mild = 0
		return [_mild, _moderate, _frequent]

	def object_as_dict(self, obj):
		return {c.key: getattr(obj, c.key)
				for c in inspect(obj).mapper.column_attrs}

	def _generateMaping(self, stateCode):
		_query = States.query.all()
		_query = StatesSchema.dump(_query).data
		return _query


class AudienceResource(Resource):
	queryArgs = {
		"Level_1": fields.Str(),
		"Level_2": fields.Str(),
		"name": fields.Str(),
		"location": fields.Str(),
		"audience": fields.Str(),
		"frequency": fields.List(fields.Str()),
		"states": fields.List(fields.Str())
	}
	def anayzedata(self, response, fmap):
		if fmap == [1, 1, 0] or [1,0,1] or [0,1,1]:
			for x in response:
				#y = x['ChainID']
				q = x['state']
				count = 0
				for z in response:
					if z['state'] == q:
						count += z['AudienceTotal']
				x['count'] = count
			return response
		else:
			return response

	def _get(self, code):
		states = States.query.filter_by(abv=code).all()
		states = schema_states.dump(states).data
		if len(states) >=1:
			return states[0]
		else:
			return {}
	def parseFrequency(self, frequency):
		_mild = 0
		_frequent = 0
		_moderate = 0 
		if len(frequency) == 3:
			return False
		if 'Frequent' in frequency:
			_frequent = 1
		if 'Moderate' in frequency:
			_moderate = 1
		if 'Mild' in frequency:
			_mild = 1
		return [_mild, _moderate, _frequent]

	@use_args(queryArgs)
	def get(self, args):
		name = ""
		Level_1 = ""
		Level_2 = ""
		if 'name'in args:
			name = args['name']
		if 'Level_1'in args:
			level_1 = args['Level_1']
		if 'Level_2'in args:
			level_2 = args['Level_2']
   
		if 'location' in args and not args['location'] == "":
			res = VistorChainsTotal.query.filter_by(LOCATION=args['location']).all()
			result = visitor_chain_schema.dump(res).data
		elif 'Level_2' in args and not args['Level_2'] == "":
			res = VistorLevel.query.filter_by(Level_2=args['Level_2']).all()
			result = visitor_level_schema.dump(res).data

		elif 'Level_1' in args and not args['Level_1'] == "":
			res = VistorLevel.query.filter_by(Level_1=args['Level_1']).all()
			result = visitor_level_schema.dump(res).data
		else:
			res = VistorChainsTotal.query.all()
			result = visitor_chain_schema.dump(res).data
		audience = ""
		frequency = []
		states = []
		_response = []
  
		if 'audience' in args:
			audience = args['audience']
		if 'states' in args:
			states = args['states']
		if 'frequency' in args:
			frequency = args['frequency']
		if audience == 'states' and len(states) >= 1 and len(res) >= 1:
			for index, _rep in enumerate(result):
				if _rep['state'] in states:
					_response.append(_rep)
		else:
			_response = result
		frequencyMap=[]
		if len(frequency) >= 1:
			frequencyMap = self.parseFrequency(frequency)
			if frequencyMap:
				if frequencyMap == [1, 0, 0]:
					_response = [i for i in _response if (i['Mild'] == 1)]
				elif frequencyMap == [0, 1, 0]:
					_response = [i for i in _response if (i['Moderate'] == 1)]
				elif frequencyMap == [0, 0, 1]:
					_response = [i for i in _response if (i['Frequent'] == 1)]
				elif frequencyMap == [1, 1, 0]:
					_response = [i for i in _response if (
						i['Mild'] == 1 and i['Moderate'] == 1)]
				elif frequencyMap == [1, 0, 1]:
					_response = [i for i in _response if (
						i['Mild'] == 1 and i['Frequent'] == 1)]
				elif frequencyMap == [0, 1, 1]:
					_response = [i for i in _response if (
						i['Moderate'] == 1 and i['Frequent'] == 1)]
		
		if len(_response) >= 1:
			for x, y in enumerate(_response):
				y['_map'] = self._get(y['state'])

		ananyzlized = self.anayzedata(_response,frequencyMap)
		metadata = {
			'queryname': name,
			'queries': {
				'audience': audience,
				'Level_1': Level_1,
				'Level_2': Level_2,
				'frequecy': dict(zip([i for i in range(0,len(frequency))], frequency)),
				'states': dict(zip([i for i in range(0, len(states))], states))
			},
			'time': str(datetime.datetime.now().timestamp())
			}
		return {"message": "Success", 'args':args ,'data': ananyzlized, 'meta':metadata}, 200

