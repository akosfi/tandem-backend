from flask import request
from functools import wraps 



def create_response_object(status, message): 
    mock = {
        'status': status,
        'message': message,
    }
    return mock

