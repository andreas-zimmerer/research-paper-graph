from flask_restplus import Namespace, fields

class PaperDto:
    api = Namespace('paper', description='paper related operations')
    paper = api.model('paper', {
        'id': fields.String(required=True, description='paper id'),
        'title': fields.String(required=True, description='paper title'),
        'abstract': fields.String(required=True, description='paper title'),
        'year': fields.Integer(required=True, description='paper year'),
        'authors': fields.List(fields.String, default=[]),
    })

class ReferenceDto:
    api = Namespace('reference', description='reference related operations')
    reference = api.model('reference', {
        'from_paper': fields.String(required=True, description='referencing paper'),
        'to_paper': fields.String(required=True, description='referenced paper'),
    })

class RelativeDto:
    api = Namespace('relative', description='relative related operations')
    relative = api.model('relative', {
        'id': fields.String(required=True, description='relative id'),
        'title': fields.String(required=True, description='relative title'),
        'abstract': fields.String(required=True, description='relative title'),
        'year': fields.Integer(required=True, description='relative year'),
        'citations': fields.List(fields.String),
        'authors': fields.List(fields.String),
    })
