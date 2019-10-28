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

class EventDto:
    api = Namespace('event', description='Event related operations.')

    event = api.model('event', {
        'name': fields.Integer(required=True),
        'date': fields.DateTime(required=True),
        'public': fields.Boolean(required=True),
        'location': fields.String(required=True),
        'details': fields.String(required=True),
        'id': fields.Integer()
    })  

    event_detailed = api.model('event_detailed', {
        'name': fields.Integer(required=True),
        'date': fields.DateTime(required=True),
        'public': fields.Boolean(required=True),
        'location': fields.String(required=True),
        'details': fields.String(required=True),
        'cover_photo': field.String(required=True),
        'people_going': field.Integer(required=True)
    })