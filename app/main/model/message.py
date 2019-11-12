from .. import db
from enum import Enum

class MessageType(str, Enum):
    TEXT: str = "TEXT"
    IMAGE: str = "IMAGE"

class Message(db.Model):
    """ Message Model for storing message related details """
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sent_at = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(1023), nullable=False)
    message_type = db.Column(db.Enum(MessageType))

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'))