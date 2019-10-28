from flask import request, after_this_request
from flask_restplus import Resource


from app.main.model.message import Message


from ..util.dto import MessageDto

from ..service.message_service import get_messages_of_user

api = MessageDto.api
_message = MessageDto.message


@api.route('/')
class UserList(Resource):
    def get(self):
        """List of all messages"""
        return get_messages_of_user(1) #!