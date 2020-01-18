"""Family Controller"""
from flask_restplus import Resource

from ..dto.relativeDto import RelativeDto
from ..service.family_service import get

api = RelativeDto.api
_relative = RelativeDto.relative

@api.route('/<relative>/<distance>/<year>')
class Family(Resource):
    """Handle a paper family."""
    @api.response(200, 'The family of the paper has been listed.')
    @api.response(404, 'The paper has not been found.')
    @api.doc('List the family of the paper.')
    @api.marshal_with(_relative)
    def get(self, relative, distance, year):
        """List all relatives of a paper."""
        return get(relative, distance, year)
