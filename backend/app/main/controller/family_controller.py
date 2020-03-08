"""Family Controller"""
from flask import request
from flask_restplus import Resource

from ..dto.relativeDto import RelativeDto
from ..service.family_service import get_preceding, get_succeeding, get_entire

api = RelativeDto.api
_relative = RelativeDto.relative

@api.route('/preceding/')
class PrecedingFamily(Resource):
    """Handle a preceding paper family."""
    @api.response(200, 'The preceding family of the paper has been listed.')
    @api.response(404, 'The paper has not been found.')
    @api.doc('List the preceding family of the paper.',
             params={'paper': 'Paper',
                     'distance': 'Distance',
                     'year': 'Year',
                     'citations': 'Citations'})
    @api.marshal_with(_relative)
    def get(self):
        """List all preceding relatives of a paper."""
        relative = request.args.get('paper')
        distance = request.args.get('distance')
        year = request.args.get('year')
        citations = request.args.get('citations')

        return get_preceding(relative, distance, year, citations)

@api.route('/succeeding/')
class SucceedingFamily(Resource):
    """Handle a succeeding paper family."""
    @api.response(200, 'The succeeding family of the paper has been listed.')
    @api.response(404, 'The paper has not been found.')
    @api.doc('List the succeeding family of the paper.',
             params={'paper': 'Paper',
                     'distance': 'Distance',
                     'year': 'Year',
                     'citations': 'Citations'})
    @api.marshal_with(_relative)
    def get(self):
        """List all succeeding relatives of a paper."""
        relative = request.args.get('paper')
        distance = request.args.get('distance')
        year = request.args.get('year')
        citations = request.args.get('citations')

        return get_succeeding(relative, distance, year, citations)

@api.route('/entire/')
class EntireFamily(Resource):
    """Handle an entire paper family."""
    @api.response(200, 'The entire family of the paper has been listed.')
    @api.response(404, 'The paper has not been found.')
    @api.doc('List the entire family of the paper.',
             params={'paper': 'Paper',
                     'distance': 'Distance',
                     'year': 'Year',
                     'citations': 'Citations'})
    @api.marshal_with(_relative)
    def get(self):
        """List all preceding relatives of a paper."""
        relative = request.args.get('paper')
        distance = request.args.get('distance')
        year = request.args.get('year')
        citations = request.args.get('citations')

        return get_entire(relative, distance, year, citations)
