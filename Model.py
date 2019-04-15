from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()

class States(db.Model):
    __tablename__ = 'geo_states'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    abv = db.Column(db.String(2), unique=True, nullable=False, primary_key=True)
    country = db.Column(db.String(2), nullable=False)
    is_state = db.Column(db.String(1), nullable=False)
    is_lower48 = db.Column(db.String(1), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)

    def __init__(self, name, abv, latitude, longitude):
        self.name = name
        self.abv = abv
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<abv {}>'.format(self.abv)
    
    def __str__(self):
        return '%s' % self.abv
    


class VistorLevel(db.Model):
    __tablename__ = 'bi-vsistor-level-totals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.String(2) )
    Level_1 = db.Column(db.String)
    Level_2 = db.Column(db.String)
    Mild = db.Column(db.Integer)
    Moderate = db.Column(db.Integer)
    Frequent = db.Column(db.Integer)
    AudienceTotal = db.Column(db.Integer)
    
    def __init__(self,state):
        self.state = state
    def __str__(self):
        return '%s' % self.state

    def __repr__(self):
        return '<state %r>' % self.state


class VistorLevelSchema(ma.Schema):
    state = fields.String()
    Level_1 = fields.String()
    Level_2 = fields.String()
    Mild = fields.Integer()
    Moderate = fields.Integer()
    Frequent = fields.Integer()
    AudienceTotal = fields.Integer()



class VistorChainsTotal(db.Model):
    __tablename__ ='bi-vistor-chain-totals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.String(2))
    ChainID = db.Column(db.Integer)
    LOCATION = db.Column(db.String)
    Mild = db.Column(db.Integer)
    Moderate = db.Column(db.Integer)
    Frequent = db.Column(db.Integer)
    AudienceTotal = db.Column(db.Integer)

    def __init__(self,state):
        self.state = state
 
class VisitorChainTotalSchma(ma.Schema):
    state = fields.String()
    ChainID = fields.Integer()
    LOCATION = fields.String()
    Mild = fields.Integer()
    Moderate = fields.Integer()
    Frequent = fields.Integer()
    AudienceTotal = fields.Integer()
    
class VisitorAudienceTotal(ma.Schema):
    AudienceTotal = fields.Integer()
    
class Vistor(db.Model):
    __tablename__ ='Visitors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID = db.Column(db.String, nullable=False)
    state = db.Column(db.String(2))
    Level_1 = db.Column(db.String)
    Level_2 = db.Column(db.String)
    ChainID = db.Column(db.Float)
    LOCATION = db.Column(db.String)
    Mild = db.Column(db.Integer)
    Moderate = db.Column(db.Integer)
    Frequent = db.Column(db.Integer)
    
    def __init__(self,state):
        self.state = state
 
class VisitorSchma(ma.Schema):
    ID = fields.String()
    state = fields.String()
    ChainID = fields.Float()
    LOCATION = fields.String()
    Mild = fields.Integer()
    Moderate = fields.Integer()
    Frequent = fields.Integer()
    AudienceTotal = fields.Integer()
    Level_2 = fields.String()
    Level_1 = fields.String()


class StatesSchema(ma.Schema):
    name = fields.String()
    abv = fields.String()
    latitude = fields.Float()
    longitude = fields.Float()


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id', ondelete='CASCADE'), nullable=False)
    category = db.relationship(
        'Category', backref=db.backref('comments', lazy='dynamic'))

    def __init__(self, comment, category_id):
        self.comment = comment
        self.category_id = category_id


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class CategorySchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class CommentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    category_id = fields.Integer(required=True)
    comment = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()
