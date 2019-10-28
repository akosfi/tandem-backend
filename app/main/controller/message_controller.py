from flask import request, after_this_request
from flask_restplus import Resource


from app.main.model.message import Message


from ..util.dto import UserDto #!!!

from ..service.message_service import get_messages_of_user



@api.route('/')
class UserList(Resource):
    def get(self):
        """List all registered users"""
        return 'a'