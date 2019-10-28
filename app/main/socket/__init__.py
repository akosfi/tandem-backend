from flask_socketio import SocketIO, emit
from flask import request

from ..service.socket_service import save_new_socket, get_user_by_socket_id, remove_socket

def create_socket_app(app):
    socketio = SocketIO(app, cors_allowed_origins="*")
     
    @socketio.on('connect')
    def connect():
        emit('CONNECT')



    @socketio.on('disconnect')
    def disconnect(): 
       socket = get_user_by_socket_id(request.sid)
       remove_socket(socket.id) 


    @socketio.on('IDENTIFY')
    def identify(data):
        save_new_socket(data, request.sid)


    @socketio.on('IM')
    def sendMessage(data): 
        socket = 

    return socketio

