from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__, static_url_path='')
    app.config.from_object(config_by_name[config_name])
    app.config['UPLOAD_FOLDER'] = 'static/img'

    db.init_app(app)
    flask_bcrypt.init_app(app)

    @app.route('/img/<path:path>')
    def send_img(path):
        return send_from_directory('static/img', path)

    return app

    