"""Database controller for references"""
from flask import request
from flask_restplus import Resource

from ..dto.dto import ReferenceDto
from ..service.reference_service import post, get_all, delete, get, delete_all

api = ReferenceDto.api
_reference = ReferenceDto.reference

@api.route('/')
class References(Resource):
    """Handle all references"""
    @api.response(200, 'All references have been listed.')
    @api.doc('List all references.')
    @api.marshal_list_with(_reference, envelope='data')
    def get(self):
        """List all references."""
        return get_all()

    @api.response(201, 'The reference has been created.')
    @api.response(409, 'The reference already exists.')
    @api.doc('Create a new reference.')
    @api.expect(_reference, validate=True)
    def post(self):
        """Create a new reference."""
        data = request.json
        return post(data=data)

    @api.response(200, 'All references have been deleted.')
    @api.doc('Delete all references.')
    @api.marshal_list_with(_reference, envelope='data')
    def delete(self):
        """Delete all references."""
        return delete_all()

@api.route('/<source>/<sink>')
class Reference(Resource):
    """Handle one reference."""
    @api.response(200, 'The reference has been found.')
    @api.response(404, 'The reference has not been found.')
    @api.doc('Display the reference you are looking for.')
    @api.marshal_with(_reference)
    def get(self, source, sink):
        """Display the reference you are looking for."""
        reference = get(source, sink)
        if not reference:
            return api.abort(404)
        return reference

    @api.response(200, 'The reference has been deleted.')
    @api.response(404, 'The reference has not been found.')
    @api.doc('Delete the reference you are looking for.')
    @api.marshal_with(_reference)
    def delete(self, source, sink):
        """Delete the reference you are looking for."""
        reference = self.get(source, sink)
        delete(source, sink)
        return reference
