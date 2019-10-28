from app.main import db
from app.main.model.message import Message


import datetime

def save_message(sender_id, target_id, message, sent_at):
    new_message = Message(
            sender_id=sender_id,
            target_id=target_id,
            message=message,
            sent_at=datetime.datetime.now()
        )

    save_changes(new_message)

def get_messages_of_user(user_id):
    return Message.query.filter_by((Message.sender_id == user_id | Message.target_id == user_id)).all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()