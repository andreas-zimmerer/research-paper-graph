"""Database controller for references"""
from flask import request
from flask_restplus import Resource

from ..util.dto import ReferenceDto
from ..service.reference_service import save_new_reference, get_all_references

api = ReferenceDto.api # pylint: disable=invalid-name
_reference = ReferenceDto.reference # pylint: disable=invalid-name

@api.route('/')
class ReferenceList(Resource):
    """Class for all references"""
    @api.doc('list_of_registered_references')
    @api.marshal_list_with(_reference, envelope='data')
    def get(self): # pylint: disable=no-self-use
        """List all registered references"""
        return get_all_references()

    @api.response(201, 'Reference successfully created.')
    @api.doc('create a new reference')
    @api.expect(_reference, validate=True)
    def post(self): # pylint: disable=no-self-use
        """Creates a new Reference"""
        data = request.json
        return save_new_reference(data=data)
