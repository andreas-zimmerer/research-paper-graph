"""Write Controller"""
from flask import request
from flask_restplus import Resource

from ..dto.writeDto import WriteDto
from ..service.write_service import post, get_all, delete, get, delete_all

api = WriteDto.api
_write = WriteDto.write

@api.route('/')
class Writes(Resource):
    """Handle all writing relations"""
    @api.response(200, 'All writing relations have been listed.')
    @api.doc('List all writing relations.')
    @api.marshal_list_with(_write, envelope='data')
    def get(self):
        """List all writing relations."""
        return get_all()

    @api.response(201, 'The writing relation has been created.')
    @api.response(409, 'The writing relation already exists.')
    @api.doc('Create a new writing relation.')
    @api.expect(_write, validate=True)
    def post(self):
        """Create a new writing relation."""
        data = request.json
        return post(data=data)

    @api.response(200, 'All writing relations have been deleted.')
    @api.doc('Delete all writing relations.')
    @api.marshal_list_with(_write, envelope='data')
    def delete(self):
        """Delete all writing relations."""
        return delete_all()

@api.route('/<paper>/<author>')
class Write(Resource):
    """Handle one writing relation."""
    @api.response(200, 'The writing relation has been found.')
    @api.response(404, 'The writing relation has not been found.')
    @api.doc('Display the writing relation you are looking for.')
    @api.marshal_with(_write)
    def get(self, paper, author):
        """Display the writing relation you are looking for."""
        write = get(paper, author)
        if not write:
            return api.abort(404)
        return write

    @api.response(200, 'The writing relation has been deleted.')
    @api.response(404, 'The writing relation has not been found.')
    @api.doc('Delete the writing relation you are looking for.')
    @api.marshal_with(_write)
    def delete(self, paper, author):
        """Delete the writing relation you are looking for."""
        write = self.get(paper, author)
        delete(paper, author)
        return write
