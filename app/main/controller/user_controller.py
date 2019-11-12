import jwt
import json

from flask import request, after_this_request
from flask_restplus import Resource
from functools import wraps 

from app.main.model.user import User

from ..util import create_response_object, jwt_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, set_user_preferences, get_all_users, get_a_user, authenticate_user, authenticate_thirdparty_user ,set_user_cookies
from ..service.socket_service import get_active_users
from ..config import key

api = UserDto.api
_user = UserDto.user



@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/me')
class UserMe(Resource):

    @jwt_required
    def get(self):
        jwt_auth_token = request.cookies.get('jwt_auth')
        payload = jwt.decode(jwt_auth_token, key)
        return payload, 200


@api.route('/active')
class UsersActive(Resource):
    @api.marshal_list_with(_user, envelope='users')
    def get(self):
        
        return get_active_users(), 200



@api.route('/login')
class UserLogin(Resource):
    def post(self):
        data = request.json
        user = authenticate_user(data)

        if not user:
            return create_response_object(401, 'Unauthorized.'), 401
        else: 
            jwt_user = set_user_cookies(user)
            return jwt_user, 200


@api.route('/third-party')
class UserThirdPartyLogin(Resource):
    def post(self):
        data = request.json
        user = authenticate_thirdparty_user(data)

        if not user:
            return create_response_object(401, 'Unauthorized.'), 401
        else: 
            jwt_user = set_user_cookies(user)
            return jwt_user, 200


@api.route('/preferences')
class UserPreferences(Resource):

    @jwt_required
    def post(self):
        data = request.json
        
        jwt_auth_token = request.cookies.get('jwt_auth')
        payload = jwt.decode(jwt_auth_token, key)

        return set_user_preferences(payload['user']['id'], data)


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class UserEntity(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, id):
        """get a user given its identifier"""
        user = get_a_user(id)
        if not user:
            api.abort(404)
        else:
            return user


    