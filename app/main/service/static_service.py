from app.main.model.language import Language
from app.main.model.topic import Topic 
from app.main.model.learning_goal import LearningGoal

def get_all_languages():
    return Language \
            .query \
            .all()

def get_all_topics():
    return Topic \
            .query \
            .all()

def get_all_learning_goals():
    return LearningGoal \
            .query \
            .all()

