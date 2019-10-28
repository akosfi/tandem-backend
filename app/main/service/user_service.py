import uuid
import datetime

from app.main import db
from app.main.model.user import User

from ..util import create_response_object


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            email=data['email'],
            full_name=data['full_name'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return create_response_object(201, 'Successfully registered.'), 201
    else:
        return create_response_object(409, 'User already exists. Please Log in.'), 409


def get_all_users():
    return User.query.all()


def authenticate_user(data): 
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return None
    else: 
        if user.check_password(data['password']):
            return user
        else: 
            return None

def get_a_user(id):
    return User.query.filter_by(id=id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()