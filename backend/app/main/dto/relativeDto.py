from flask_restplus import Namespace, fields

class RelativeDto:
    api = Namespace('family', description='Manage families')
    relative = api.model('relative', {
        'id': fields.String(required=True, description='relative id'),
        'title': fields.String(required=True, description='relative title'),
        'abstract': fields.String(required=True, description='relative title'),
        'year': fields.Integer(required=True, description='relative year'),
        'citations': fields.List(fields.String),
        'authors': fields.List(fields.String),
    })
