import jwt
import json
import requests
import re

from flask import request, after_this_request, jsonify
from flask_restplus import Resource
from functools import wraps 

from app.main.model.user import User, AuthType

from ..util import create_response_object, jwt_required, upload_image, get_user_from_request
from ..util.dto import UserDTO
from ..service.user_service import add_known_user, save_new_user, get_known_users, set_user_preferences, set_user_profile_picture, get_all_users, get_recommended_users, get_a_user, authenticate_user, authenticate_thirdparty_user ,set_user_cookies
from ..service.socket_service import get_active_users
from ..config import key

api = UserDTO.api


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(UserDTO.user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(UserDTO.user_registration, validate=True)
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
    
    @api.marshal_list_with(UserDTO.user, envelope='users')
    @jwt_required
    def get(self):
        user = get_user_from_request(request)

        return get_active_users(user['id']), 200


@api.route('/recommended')
class UsersRecommended(Resource):

    @api.marshal_list_with(UserDTO.user, envelope='users')
    @jwt_required
    def get(self):
        user = get_user_from_request(request)

        return get_recommended_users(user['id']), 200


@api.route('/known')
class UsersKnown(Resource):

    @api.marshal_list_with(UserDTO.user, envelope='users')
    @jwt_required
    def get(self):
        user = get_user_from_request(request)

        return get_known_users(user['id']), 200

@api.route('/<id>/add')
class UsersAddToKnown(Resource):

    @jwt_required
    def get(self, id):
        user = get_user_from_request(request)

        return add_known_user(user['id'], id), 200


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

        if data['auth_type'] == AuthType.T_FACEBOOK:
            url='https://graph.facebook.com/v2.3/me'
            params = {'access_token': data['access_token'], 'fields': 'name,email,picture.width(800).height(800)'}

            response = requests.get(url, params).json()

            data['full_name'] = response['name']
            data['email'] = response['email']
            
            data['profile_pic_url'] = response['picture']['data']['url']

        else: 
            url = 'https://www.googleapis.com/oauth2/v3/userinfo'
            params = {'access_token': data['access_token'], 'alt': 'json'}

            response = requests.get(url, params).json()

            data['full_name'] = response['name']
            data['email'] = response['email']
            data['profile_pic_url'] = response['picture']
        
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
        
        user = get_user_from_request(request)

        return set_user_preferences(user['id'], data)



@api.route('/picture')
class UserPicture(Resource):

    @jwt_required
    def post(self):
        data = request.json
        
        user = get_user_from_request(request)

        profile_picture = upload_image(request)

        set_user_profile_picture(user['id'], profile_picture)

        return create_response_object(200, 'Image uploaded succesfully.', profile_picture), 200


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class UserEntity(Resource):
    @api.doc('get a user')
    @api.marshal_with(UserDTO.user)
    def get(self, id):
        """get a user given its identifier"""
        user = get_a_user(id)
        if not user:
            api.abort(404)
        else:
            return user


    