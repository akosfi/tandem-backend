from .. import db

class Language(db.Model):
    """ Language Model for storing language related details """
    __tablename__ = "language"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)