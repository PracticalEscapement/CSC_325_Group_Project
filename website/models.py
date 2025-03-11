from . import db
from flask_login import UserMixin


class user(db.Model,UserMixin):
    id = db.Column(db.String(150),primary_key=True)
    email= db.Column(db.String(150), nullable=False)
    username= db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
