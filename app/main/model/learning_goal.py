from .. import db

class LearningGoal(db.Model):
    """ LearningGoals Model for storing learning goals related details """
    __tablename__ = "learning_goal"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)