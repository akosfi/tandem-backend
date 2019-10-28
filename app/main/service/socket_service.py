from app.main import db
from app.main.model.socket_user import SocketUser
from app.main.model.user import User


def save_new_socket(db_id, socket_id):
    socket = SocketUser.query.filter_by(user_db_id=db_id).first()

    if socket:
        socket.user_socket_id = socket_id
        db.session.commit()

    else:
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


def get_active_users(): 

    return SocketUser.query.join(User, User.id == SocketUser.user_db_id).with_entities(User.email, User.full_name, User.id, User.profile_pic_url).all()
    #return SocketUser.query.with_entities(SocketUser.id, SocketUser.user_db_id, SocketUser.user_socket_id).all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()