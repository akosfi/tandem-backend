import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS

from app import blueprint
from app.main import create_app, create_socket_app, db
from app.main.model import user, event, connection, language, message

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

CORS(app, supports_credentials=True)

app.app_context().push()

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)


#//////////////////////////////////////
"""@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response"""
#//////////////////////////////////////

@manager.command
def run():
    
    #app.run()
    socketapp = create_socket_app(app)
    socketapp.run(app, host="localhost")

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
