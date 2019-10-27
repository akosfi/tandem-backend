import jwt

from flask import request
from flask_restplus import Resource

from app.main.model.user import User

from ..util import create_response_object
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, authenticate_user
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




@api.route('/login')
class UserLogin(Resource):
    def post(self):
        data = request.json
        user = authenticate_user(data)

        if not user:
            return create_response_object(401, 'Unauthorized.'), 401
        else: 
            jwt_auth = user.encode_auth_token('tomi')
            jwt_user = 'tomi'

            return 'user', 200, {'Set-Cookie': f'jwt_auth={jwt_auth}; HttpOnly', 'Set-Cookie': f'jwt_user={jwt_user}; Max-Age=180000000'} #!!!





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


    