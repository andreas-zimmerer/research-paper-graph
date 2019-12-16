"""Database controller for relatives"""
from flask_restplus import Resource

from ..util.dto import RelativeDto
from ..service.relative_service import get_all_relatives

api = RelativeDto.api # pylint: disable=invalid-name
_relative = RelativeDto.relative # pylint: disable=invalid-name

@api.route('/<title>')
@api.param('title', 'The Paper title')
@api.response(404, 'Paper not found.')
class Relative(Resource):
    """Class for one paper"""
    @api.doc('get a relative')
    @api.marshal_with(_relative)
    def get(self, title): # pylint: disable=no-self-use
        """get a paper given its title"""
        return get_all_relatives(title)