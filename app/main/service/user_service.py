import uuid
import datetime
import json

from flask import after_this_request

from sqlalchemy.orm import aliased

from app.main import db
from app.main.model.user import User
from app.main.model.language import Language

from ..util import create_response_object


def save_new_user(data):
    user = User \
            .query \
            .filter_by(email=data['email']) \
            .first()
    
    if not user:
        new_user = User(
            email=data['email'],
            full_name=data['full_name'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow(),
            registration_finished=False
        )
        save_changes(new_user)
        
        jwt_user = set_user_cookies(new_user)
        
        return create_response_object(201, 'Successfully registered.', jwt_user), 201
    else:
        return create_response_object(409, 'User already exists. Please Log in.'), 409


def get_all_users():
    return User \
            .query \
            .all()

def get_recommended_users(id):
    friendUser = aliased(User)
    known_user_ids = db \
                        .session \
                        .query(User) \
                        .filter(User.id == id) \
                        .join((friendUser), User.friends) \
                        .with_entities(friendUser.id)

    return User \
            .query \
            .filter(User.id != id) \
            .filter(~User.id.in_(known_user_ids)) \
            .all()


def get_known_users(id):
    return User \
            .query \
            .filter_by(id=id) \
            .first() \
            .friends


def add_known_user(my_id, user_id):
    user = db.session.query(User) \
            .filter_by(id=my_id) \
            .first()

    user_to_add = db.session.query(User) \
                    .filter_by(id=user_id) \
                    .first()

    user.befriend(user_to_add)

    db.session.commit()

    return create_response_object(200, "User added to known users")

    


def authenticate_user(data): 
    user = User \
            .query \
            .filter_by(email=data['email']) \
            .first()

    if not user:
        return None
    else: 
        if user.check_password(data['password']):
            return user
        else: 
            return None


def authenticate_thirdparty_user(data):
    user = User \
            .query \
            .filter_by(email=data['email'], auth_type=data['auth_type']) \
            .first()


    if not user:
        new_user = User(
            email=data['email'],
            full_name=data['full_name'],
            access_token=data['access_token'],
            auth_type=data['auth_type'],
            registered_on=datetime.datetime.utcnow(),
            registration_finished=False,
            profile_pic_url=data['profile_pic_url']
        )
        save_changes(new_user)
        return new_user
    else:
        return user


def get_a_user(id):
    return User \
            .query \
            .filter_by(id=id) \
            .first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()



def set_user_cookies(user): 
    jwt_user = {
        'id': str(user.id),
        'email': user.email,
        'profile_pic_url': user.profile_pic_url,
        'full_name': user.full_name,
        'registration_finished': user.registration_finished,
    }
    jwt_auth = user.encode_auth_token(jwt_user)

    @after_this_request
    def set_jwt_cookies(response):
        response.set_cookie('jwt_auth', jwt_auth, httponly=True)
        response.set_cookie('jwt_user', json.dumps(jwt_user), max_age=180000000)
        return response

    return jwt_user



def set_user_preferences(id, data): 
    user = db.session.query(User) \
            .filter_by(id=id) \
            .first()

    for language in data['nativeLanguages']:
        language = Language.query.filter_by(id=language['id']).first()
        user.user_native_languages.append(language)

    for language in data['fluentLanguages']:
        language = Language.query.filter_by(id=language['id']).first()
        user.user_known_languages.append(language)

    for language in data['goalLanguages']:
        language = Language.query.filter_by(id=language['id']).first()
        user.user_goal_languages.append(language)

    
    user.registration_finished = True
    db.session.commit()     

    jwt_user = set_user_cookies(user)
    return jwt_user, 200


def set_user_profile_picture(id, picture): 
    user = db.session.query(User) \
            .filter_by(id=id) \
            .first()

    user.profile_pic_url = picture

    db.session.commit()

    set_user_cookies(user)

    return picture

    
