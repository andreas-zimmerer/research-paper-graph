"""Control all backend features"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

def create_app(config_name):
    """Initialize the backend"""
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app

