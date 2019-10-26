from .. import db

class Event(db.Model):
    """ Event Model for storing event related details """
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    details = db.Column(db.String(1023), nullable=False)
    cover_photo = db.Column(db.String(255), nullable=False)

    #userid