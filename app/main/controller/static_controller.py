import os

from flask import send_from_directory, request
from flask_restplus import Resource
from werkzeug.utils import secure_filename

from ..util import get_unique_filename, allowed_file, jwt_required, create_response_object
from ..util.dto import StaticDTO
from ..config import key, basedir
from ..service.static_service import get_all_languages, get_all_learning_goals, get_all_topics

api = StaticDTO.api


@api.route('/languages')
class LanguageList(Resource):
    @api.doc('list_of_languages')
    @api.marshal_list_with(StaticDTO.language, envelope='languages')
    def get(self):
        """List all events"""
        return get_all_languages()


@api.route('/learning_goals')
class LanguageList(Resource):
    @api.doc('list_of_learning_goals')
    @api.marshal_list_with(StaticDTO.learning_goal, envelope='learning_goals')
    def get(self):
        """List all learning_goals"""
        return get_all_learning_goals()



@api.route('/topics')
class LanguageList(Resource):
    @api.doc('list_of_topics')
    @api.marshal_list_with(StaticDTO.topic, envelope='topics')
    def get(self):
        """List all topics"""
        return get_all_topics()

