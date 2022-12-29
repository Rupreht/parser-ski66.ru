""" models.py """

from datetime import datetime
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
        return '<User %r>' % self.username

class Post(db.Model):
    """ class Post """
    id            = db.Column(db.Integer, primary_key=True)
    ovner         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    forward       = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    title         = db.Column(db.String(256), default='', nullable=False)
    pub_date      = db.Column(db.DateTime, default=datetime.now())
    last_modified = db.Column(db.DateTime, default=datetime.now(),
                              onupdate=datetime.now())
    sity          = db.Column(db.String(80), default='', nullable=False)
    content       = db.Column(db.Text, default='', nullable=False)
    typograf      = db.Column(db.Text, default='', nullable=False)

    def __init__(self, title, content, ovner) -> None:
        self.title = title
        self.content = content
        self.ovner = ovner

    def __str__(self):
        return '<Post %r>' % self.title

    def __repr__(self):
        return '<Post %r>' % self.title

    def set_title(self, title):
        self.title = title

    def set_content(self, content):
        self.content = content

    def set_pub_date(self, pub_date):
        self.pub_date = datetime.fromisoformat(pub_date).replace(microsecond=0)

    def set_sity(self, sity):
        self.sity = sity

    def set_forward(self, forward):
        self.forward = forward
