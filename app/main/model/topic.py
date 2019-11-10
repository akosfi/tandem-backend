from .. import db

class Topic(db.Model):
    """ Topic Model for storing topics related details """
    __tablename__ = "topic"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)