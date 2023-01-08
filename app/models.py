""" models.py """

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    """ class User """
    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return f'User: {self.username}'
