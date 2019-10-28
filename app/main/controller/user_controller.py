import jwt
import json

from flask import request, after_this_request
from flask_restplus import Resource
from functools import wraps 

from app.main.model.user import User

from ..util import create_response_object
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, authenticate_user
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
    def get(self):
        jwt_auth_token = request.cookies.get('jwt_auth')

        if not jwt_auth_token:
            response_object = create_response_object(409, 'No JWT token was provided.')
            return response_object, 409
        else: 
            try:
                payload = jwt.decode(jwt_auth_token, key)
                return payload, 200
            except jwt.ExpiredSignatureError:
                return create_response_object(409, 'Expired signature.'), 409
            except jwt.InvalidTokenError:
                return create_response_object(409, 'Invalid token.'), 409



@api.route('/active')
class UsersActive(Resource):
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
            jwt_user = {
                'id': str(user.id),
                'email': user.email,
                'profile_pic_url': user.profile_pic_url,
                'full_name': user.full_name
            }
            jwt_auth = user.encode_auth_token(jwt_user)

            @after_this_request
            def set_jwt_cookies(response):
                response.set_cookie('jwt_auth', jwt_auth, httponly=True)
                response.set_cookie('jwt_user', json.dumps(jwt_user), max_age=180000000)
                return response


            return jwt_user, 200





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


    