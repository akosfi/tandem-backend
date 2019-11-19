import jwt
import uuid
import os

from flask import request
from functools import wraps 
from werkzeug.utils import secure_filename

from ..config import key, basedir


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


def get_unique_filename(filename):
    
    generated = str(uuid.uuid4()) 
    extension = filename.rsplit('.', 1)[1].lower()

    return '.'.join([generated, extension]) 


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def upload_image(request): 
    if 'file' not in request.files:
        return None
    file = request.files['file']
    if file.filename == '':
        return None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = get_unique_filename(filename)
        file.save(os.path.join(basedir, 'public/img', unique_filename))
        return unique_filename