import datetime

from .. import db
from ._association_tables import user_joined_events

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
    
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship('User', secondary=user_joined_events, back_populates="events_joined")

