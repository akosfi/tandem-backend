import jwt
import os
import uuid

from flask import request, after_this_request
from flask_restplus import Resource
from werkzeug.utils import secure_filename

from app.main.model.message import Message

from ..util import jwt_required, create_response_object
from ..util.dto import MessageDto
from ..config import key, basedir
from ..service.message_service import get_messages_of_user

api = MessageDto.api
_message = MessageDto.message


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(filename):
    
    generated = str(uuid.uuid4()) 
    extension = filename.rsplit('.', 1)[1].lower()

    return '.'.join([generated, extension]) 


@api.route('/')
class MessageList(Resource):

    @jwt_required
    def get(self):
        jwt_auth_token = request.cookies.get('jwt_auth')
        payload = jwt.decode(jwt_auth_token, key)
          
        return get_messages_of_user(payload['user']['id'])


@api.route('/image')
class MessageImage(Resource): 

    @jwt_required
    def post(self):
        if 'file' not in request.files:
            return create_response_object(404, 'File not found.'), 404
        file = request.files['file']
        if file.filename == '':
            return create_response_object(404, 'File not found.'), 404
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = get_unique_filename(filename)
            file.save(os.path.join(basedir, 'static/img', unique_filename))
            return create_response_object(200, 'File uploaded succesfully.', unique_filename), 200





