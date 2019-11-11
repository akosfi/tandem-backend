from flask_restplus import Resource

from ..util.dto import StaticDto
from ..service.static_service import get_all_languages, get_all_learning_goals, get_all_topics

api = StaticDto.api
_language = StaticDto.language
_learning_goal = StaticDto.learning_goal
_topic = StaticDto.topic



@api.route('/languages')
class LanguageList(Resource):
    @api.doc('list_of_languages')
    @api.marshal_list_with(_language, envelope='languages')
    def get(self):
        """List all events"""
        return get_all_languages()


@api.route('/learning_goals')
class LanguageList(Resource):
    @api.doc('list_of_learning_goals')
    @api.marshal_list_with(_learning_goal, envelope='learning_goals')
    def get(self):
        """List all learning_goals"""
        return get_all_learning_goals()



@api.route('/topics')
class LanguageList(Resource):
    @api.doc('list_of_topics')
    @api.marshal_list_with(_topic, envelope='topics')
    def get(self):
        """List all topics"""
        return get_all_topics()
