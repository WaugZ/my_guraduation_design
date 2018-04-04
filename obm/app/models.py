from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
# from app.search import add_to_index, remove_from_index, query_index


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    models = db.relationship('Models', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def owned_models(self):
        models = Models.query.filter_by(user_id=self.id)
        return models.order_by(Models.timestamp.desc())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Models(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String)
    model_target = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data_path = db.Column(db.String)  # path to data stored in server
    model_path = db.Column(db.String)  # path to model stored in server
    statue = db.Column(db.Boolean, default=False)  # store the statue

    def complete(self):
        self.statue = True

    def __repr__(self):
        return '<Model {}>'.format(self.model_name)
