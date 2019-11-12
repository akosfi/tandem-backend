import jwt

from flask import request, after_this_request
from flask_restplus import Resource


from app.main.model.message import Message

from ..util import jwt_required
from ..util.dto import MessageDto
from ..config import key
from ..service.message_service import get_messages_of_user

api = MessageDto.api
_message = MessageDto.message


@api.route('/')
class MessageList(Resource):

    @jwt_required
    def get(self):
        jwt_auth_token = request.cookies.get('jwt_auth')
        payload = jwt.decode(jwt_auth_token, key)
          
        return get_messages_of_user(payload['user']['id'])


    