from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'full_name': fields.String(required=True, description='user full name'),
        'password': fields.String(required=True, description='user password'),
        'id': fields.String(description='user Identifier')
    })


class MessageDto:
    api = Namespace('message', description='message related operations')
    message = api.model('message', {
        'sender_id': fields.Integer(required=True),
        'target_id': fields.Integer(required=True),
        'message': fields.String(required=True),
        'sent_at': fields.DateTime()
    })