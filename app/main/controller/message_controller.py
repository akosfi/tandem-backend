import jwt
import os
import uuid

from flask import request, after_this_request
from flask_restplus import Resource
from werkzeug.utils import secure_filename

from app.main.model.message import Message

from ..util import jwt_required, create_response_object, upload_image, get_user_from_request
from ..util.dto import MessageDTO
from ..config import key, basedir
from ..service.message_service import get_messages_of_user

api = MessageDTO.api


@api.route('/')
class MessageList(Resource):

    @jwt_required
    def get(self):
        user = get_user_from_request(request)
          
        return get_messages_of_user(user['id'])


@api.route('/image')
class MessageImage(Resource): 

    @jwt_required
    def post(self):
        file = upload_image(request)

        if file is None: 
            return create_response_object(404, 'File not found.'), 404
        else:
            return create_response_object(200, 'File uploaded succesfully.', file), 200



