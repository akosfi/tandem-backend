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
    messages = Message.query.all()
    messages_response = {};

    for f in messages: 
        message_mock = {
            'sender_id': f.sender_id,
            'target_id': f.target_id,
            'message': f.message,
            'sent_at': f.sent_at.isoformat()
        }
        if f.sender_id in messages_response:
            messages_response[f.sender_id].append(message_mock)
        else:
            temp = []
            temp.append(message_mock)
            messages_response[f.sender_id] = temp


        if f.target_id in messages_response:
            messages_response[f.target_id].append(message_mock)
        else:
            temp = []
            temp.append(message_mock)
            messages_response[f.target_id] = temp

    return messages_response

def save_changes(data):
    db.session.add(data)
    db.session.commit()