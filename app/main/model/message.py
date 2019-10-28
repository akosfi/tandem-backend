from .. import db

class Message(db.Model):
    """ Message Model for storing message related details """
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sent_at = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(1023), nullable=False)

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'))