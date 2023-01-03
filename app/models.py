from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from app import db, login


class User(UserMixin, db.Model):
    _id           = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), index=True, unique=True)
    email         = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts         = db.relationship('Post', backref='author', lazy='dynamic')
    about_me      = db.Column(db.String(140))
    last_seen     = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self): # переопределенное свойство
        return (self._id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8'))
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Post(db.Model):
    _id       = db.Column(db.Integer, primary_key=True)
    body      = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id   = db.Column(db.Integer, db.ForeignKey('user._id'))

    def __repr__(self):
        return f'<Post {self.body}>'

    def get_id(self): # переопределенное свойство
        return (self._id)

@login.user_loader
def load_user(_id):
    return User.query.get(int(_id))