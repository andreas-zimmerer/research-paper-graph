from flask_restplus import Namespace, fields

class WriteDto:
    api = Namespace('write', description='Manage writing relations')
    write = api.model('write', {
        'paper': fields.String(required=True, description='paper'),
        'author': fields.String(required=True, description='author'),
    })
