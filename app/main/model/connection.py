from .. import db

class Connection(db.Model):
    """ Connect Model for storing connection related details (users who already connected) """
    __tablename__ = "connection"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id_1 = db.Column(db.Integer, nullable=False, default=0)
    user_id_2 = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=False)