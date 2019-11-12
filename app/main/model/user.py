import datetime
import jwt

from enum import Enum

from ..config import key
from .. import db, flask_bcrypt

from ..model.event import user_joined_events

user_native_language = db.Table('user_native_language',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True)
)

user_known_language = db.Table('user_known_language',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True)
)

user_goal_language = db.Table('user_goal_language',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True)
) 

class AuthType(str, Enum):
    PASSWORD: str = "PASSWORD"
    T_FACEBOOK: str = "T_FACEBOOK"
    T_GOOGLE: str = "T_GOOGLE"

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    full_name = db.Column(db.String(100))
    password_hash = db.Column(db.String(100))
    profile_pic_url = db.Column(db.String(100))
    registration_finished = db.Column(db.Boolean)
    auth_type = db.Column(db.Enum(AuthType))
    access_token = db.Column(db.String(255))


   # messages = db.relationship('Message', backref='user', lazy=True)
    #events = db.relationship('Event', backref='user', lazy=True)
    
    events_joined = db.relationship('Event', secondary=user_joined_events, back_populates="users")

    user_native_languages = db.relationship('Language', secondary=user_native_language)
    user_known_languages = db.relationship('Language', secondary=user_known_language)
    user_goal_languages = db.relationship('Language', secondary=user_goal_language)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.id)


    def encode_auth_token(self, user):
        try:
            payload = {
                'user': user
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            ).decode('utf-8')
        except Exception as e:
            return e

    @staticmethod  
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, key)
            return payload
            #is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            #if is_blacklisted_token:
            #    return 'Token blacklisted. Please log in again.'
            #else:
            #    return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
