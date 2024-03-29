import json

from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
from flask import request

from ..service.socket_service import save_new_socket, get_user_by_socket_id, remove_socket, get_user_by_db_id
from ..service.message_service import save_message


def create_socket_app(app):
    socketio = SocketIO(app, cors_allowed_origins="*")
     
    @socketio.on('connect')
    def connect():
        #print(f'CONNECT {request.sid}')
        join_room(room=request.sid, sid=request.sid)
        emit('CONNECT', room=request.sid)


    @socketio.on('disconnect')
    def disconnect():
        leave_room(room=request.sid, sid=request.sid)
        close_room(room=request.sid)

        socket = get_user_by_socket_id(request.sid)
        remove_socket(socket.id) 


    @socketio.on('IDENTIFY')
    def identify(data):
        save_new_socket(data, request.sid)


    @socketio.on('IM')
    def sendMessage(data): 
        recipient_id = data['target_id']
        socket = get_user_by_db_id(recipient_id)

        if socket:
            emit('IM', data, room=socket.user_socket_id)

        save_message(data['sender_id'], data['target_id'], data['message'], data['sent_at'], data['message_type'])

    return socketio

