import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from flask import render_template
from flask_socketio import SocketIO

from app import blueprint
from app.main import create_app, db
from app.main.model import user, event, language, topic, learning_goal, message, socket_user
from app.main.socket import create_socket_app
from app.main.util.seed import seed_languages, seed_learning_goals, seed_topics

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

CORS(app, supports_credentials=True) #!

app.app_context().push()

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)

socketio = create_socket_app(app)

@manager.command
def run():
    socketio.run(app)

@manager.command
def seed():
    seed_languages()
    seed_learning_goals()
    seed_topics()
    return 

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
