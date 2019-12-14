"""
This file serves as the point of entry for of the webserver logic.
"""

from flask import Flask
from flask_cors import CORS, cross_origin

# pylint: disable=invalid-name
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Import at bottom to prevent circular imports
# pylint: disable=wrong-import-position
from app import routes
