from .. import db

users = db.Table('user_joined_event',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

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

    users = db.relationship('User', secondary=users)


    def toDTO(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': 'fix this!!!!!',
            'public': self.public,
            'location': self.location,
            'details': self.details,
        }
