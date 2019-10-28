from .. import db


class SocketUser(db.Model):
    """ Event Model for storing event related details """
    __tablename__ = "socket_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_db_id = db.Column(db.Integer, unique=True, nullable=False)
    user_socket_id = db.Column(db.String(100), unique=True, nullable=False)