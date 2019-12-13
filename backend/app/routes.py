"""
This file provides the routes for the backend.
"""
from flask import request, jsonify
# pylint: disable=cyclic-import
from app import app

PAPERS = [
    {
        'id': 1,
        'title': 'Of Mice and Men',
        'authors': ['Dagobert', 'Donald'],
        'abstract': 'A long time ago, in a galaxy far, far away...',
        'year': 2019,
        'citations': [2, 3, 4]
    },
    {
        'id': 2,
        'title': 'A long story...',
        'authors': ['Fred'],
        'abstract': 'So here it began.',
        'year': 2015,
        'citations': []
    },
    {
        'id': 3,
        'title': 'Cinderella',
        'authors': ['Disney'],
        'abstract': 'wish, dress, prince, kiss',
        'year': 2005,
        'citations': [4]
    },
    {
        'id': 4,
        'title': 'FooBar',
        'authors': ['Google'],
        'abstract': 'A Foo walks into a Bar...',
        'year': 2012,
        'citations': [4]
    }
]

@app.route('/')
def index():
    """
    Simple example route that only prints "Hello World".
    :return: "Hello World"
    """
    return "Hello, World!"

@app.route('/search')
def search():
    """
    Searches the database for papers with the given keyword.
    """
    keyword = request.args.get('keyword')
    matching_papers = list(filter(lambda paper: keyword in paper['title'], PAPERS))
    return jsonify(matching_papers)
