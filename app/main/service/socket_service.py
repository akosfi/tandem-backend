from app.main import db
from app.main.model.socket_user import SocketUser


def save_new_socket(db_id, socket_id):
    new_socket = SocketUser(
        user_db_id=db_id,
        user_socket_id=socket_id
    )
    save_changes(new_socket)

def get_user_by_db_id(db_id):
    return SocketUser.query.filter_by(user_db_id=db_id).first()

def get_user_by_socket_id(socket_id):
    return SocketUser.query.filter_by(user_socket_id=socket_id).first()

def remove_socket(id):
    SocketUser.query.filter_by(id=id).delete()


def save_changes(data):
    db.session.add(data)
    db.session.commit()