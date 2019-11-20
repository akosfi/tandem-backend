from ..model.language import Language
from ..model.learning_goal import LearningGoal
from ..model.topic import Topic
from .. import db


languages = ['Mandarin(Chinese)','English','Spanish','Arabic','Bengali','Hindi','Russian','Portuguese','Japanese','German','Wu(Chinese)','Javanese','Korean','French','Turkish','Vietnamese','Telugu','Yue(Chinese)','Marathi','Tamil','Italian','Urdu','Min Nan(Chinese)','Jinyu(Chinese)','Gujarati','Polish','Ukrainian','Persian','Bhojpuri','Hausa','Burmese','Serbo-Croatian','Thai','Dutch','Yoruba','Sindhi','Hungarian']
topics = ['Cars', 'Politics', 'History', 'Job', 'Clothes', 'Sport', 'Free-time', 'Music', 'Movies', 'Series', 'Food', 'Travel', 'Books', 'TV', 'Hoobies', 'Children', 'Pets', 'Learning', 'Technology']
learning_goals = ['Work', 'Travel', 'School', 'Exam', 'Moving abroad', 'Fun', 'Getting to know new people']


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

