"""Control all backend features"""
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy # pylint: disable=import-error
from flask_bcrypt import Bcrypt # pylint: disable=import-error

from .config import config_by_name

# pylint: disable=invalid-name
db = SQLAlchemy()
# pylint: disable=invalid-name
flask_bcrypt = Bcrypt()

def create_app(config_name):
    """Initialize the backend"""
    app = Flask(__name__)

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app
