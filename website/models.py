from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False) 
    email= db.Column(db.String(150), unique=True, nullable=False)
    username= db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)


# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
