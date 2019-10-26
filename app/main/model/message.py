from .. import db

class Message(db.Model):
    """ Message Model for storing message related details """
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #sender id
    #target id
    sent_at = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(1023), nullable=False)