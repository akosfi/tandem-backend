from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__, 
                static_url_path='', 
                static_folder='public')
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    flask_bcrypt.init_app(app)

    @app.route('/')
    def serve_public():
        return send_from_directory('public', 'index.html')

    return app

    