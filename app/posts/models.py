""" models.py """

from datetime import datetime
from hashlib import sha1
from app import db


class Post(db.Model):
    """ Class Post """
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
    hash          = db.Column(db.String(40), default='', nullable=False)
    pub           = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    mode          = db.Column(db.String(80), default='', nullable=False)

    def __init__(self, title, content, ovner) -> None:
        self.title = title
        self.content = content
        self.ovner = ovner
        self.hash = self.get_hash()

    def __str__(self):
        return f'Post: {self.title}'

    def __repr__(self):
        return f'Post: {self.title}'

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

    def set_archive(self):
        self.forward = 3

    def get_hash(self):
        return sha1(bytes(self.content, encoding='utf8')).hexdigest()

    def set_mode(self, mode):
        self.mode = mode
