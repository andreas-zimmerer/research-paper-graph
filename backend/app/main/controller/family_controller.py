"""Family Controller"""
from flask_restplus import Resource

from ..dto.relativeDto import RelativeDto
from ..service.family_service import get_all, get_by_distance

api = RelativeDto.api
_relative = RelativeDto.relative

@api.route('/<relative>')
class Family(Resource):
    """Handle a paper family."""
    @api.response(200, 'The family of the paper has been listed.')
    @api.response(404, 'The paper has not been found.')
    @api.doc('List the family of the paper.')
    @api.marshal_with(_relative)
    def get(self, relative):
        """List all relatives of a paper."""
        return get_all(relative)

@api.route('/<relative>/<distance>')
class DistanceFamily(Resource):
    """Handle all paper relatives that are no more away than the given distance."""
    @api.response(200, 'The family of the paper has been listed.')
    @api.response(404, 'The paper has not been found.')
    @api.doc('List all paper relatives that are no more away than the given distance.')
    @api.marshal_with(_relative)
    def get(self, relative, distance):
        """List all relatives of a paper."""
        return get_by_distance(relative, distance)
