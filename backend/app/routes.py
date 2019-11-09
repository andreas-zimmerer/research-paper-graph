"""
This file provides the routes for the backend.
"""
# pylint: disable=cyclic-import
from app import app

@app.route('/')
def index():
    """
    Simple example route that only prints "Hello World".
    :return: "Hello World"
    """
    return "Hello, World!"
