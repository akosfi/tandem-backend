from .. import db

class Connection(db.Model):
    """ Connect Model for storing connection related details (users who already connected) """
    __tablename__ = "connection"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #user_1_id
    #user_2_id
    date = db.Column(db.DateTime, nullable=False)