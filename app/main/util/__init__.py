import jwt

from flask import request
from functools import wraps 

from ..config import key


def create_response_object(status, message, data = None): 
    mock = {
        'status': status,
        'message': message,
        'data': data,
    }
    return mock



def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        jwt_auth_token = request.cookies.get('jwt_auth')

        if not jwt_auth_token:
            response_object = create_response_object(409, 'No JWT token was provided.')
            return response_object, 409
        else: 
            try:
                payload = jwt.decode(jwt_auth_token, key)
            except jwt.ExpiredSignatureError:
                return create_response_object(409, 'Expired signature.'), 409
            except jwt.InvalidTokenError:
                return create_response_object(409, 'Invalid token.'), 409

        return f(*args, **kwargs)
    return decorated