""" models.py """

import datetime
from flask_login import UserMixin
from sqlalchemy import func
from . import db

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    ovner       = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_modify = db.Column(db.DateTime, onupdate=datetime.datetime.now,
                    server_default=func.sysdate())
    title       = db.Column(db.String(256))
    content     = db.Column(db.Text)

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Post %r>' % self.title

    def set_title(self, title):
        self.title = title

    def set_content(self, content):
        self.content = content
