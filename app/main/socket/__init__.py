from flask_socketio import SocketIO, emit


def create_socket_app(app):
    socketio = SocketIO(app, cors_allowed_origins="*")
     
    @socketio.on('connect')
    def connect():
        emit('CONNECT')

    return socketio

