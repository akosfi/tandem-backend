from ..model.language import Language
from ..model.learning_goal import LearningGoal
from ..model.topic import Topic
from .. import db


languages = ['Hungarian', 'German', 'Portugese']
topics = ['Cars', 'Politics', 'History']
learning_goals = ['Work', 'Travel', 'Language exam']


def seed_languages():
    for _language in languages:
        language = Language(name=_language)
        db.session.add(language)
    
    db.session.commit()


def seed_topics():
    for _topic in topics:
        topic = Topic(name=_topic)
        db.session.add(topic)
    
    db.session.commit()


def seed_learning_goals():
    for _learning_goal in learning_goals:
        learning_goal = LearningGoal(name=_learning_goal)
        db.session.add(learning_goal)
    
    db.session.commit()

