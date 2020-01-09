from flask_restplus import Namespace, fields

class PaperDto:
    api = Namespace('paper', description='Manage papers')
    paper = api.model('paper', {
        'id': fields.String(required=True, description='paper id'),
        'title': fields.String(required=True, description='paper title'),
        'abstract': fields.String(required=True, description='paper title'),
        'year': fields.Integer(required=True, description='paper year'),
    })
