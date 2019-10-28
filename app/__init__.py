from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.message_controller import api as message_ns


blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service',
          doc='/doc/'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(message_ns, path='/message')