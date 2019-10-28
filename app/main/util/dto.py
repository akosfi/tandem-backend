from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'full_name': fields.String(required=True, description='user full name'),
        'password': fields.String(required=True, description='user password'),
        'id': fields.String(description='user Identifier')
    })