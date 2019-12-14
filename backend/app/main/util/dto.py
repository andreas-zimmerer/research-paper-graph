from flask_restplus import Namespace, fields

class PaperDto:
    api = Namespace('paper', description='paper related operations')
    paper = api.model('paper', {
        'title': fields.String(required=True, description='paper title'),
        'abstract': fields.String(required=True, description='paper title'),
        'year': fields.Integer(required=True, description='paper year'),
    })