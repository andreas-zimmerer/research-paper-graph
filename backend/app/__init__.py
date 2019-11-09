"""
This file serves as the point of entry for of the webserver logic.
"""

from flask import Flask

# pylint: disable=invalid-name
app = Flask(__name__)

# Import at bottom to prevent circular imports
# pylint: disable=wrong-import-position
from app import routes
