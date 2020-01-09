from flask_restplus import Namespace, fields

class AuthorDto:
    api = Namespace('author', description='Manage authors')
    author = api.model('author', {
        'id': fields.String(required=True, description='author id'),
        'name': fields.String(required=True, description='author name')
    })