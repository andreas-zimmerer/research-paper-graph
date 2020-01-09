"""Author Controller"""
from flask_restplus import Resource
from flask import request

from ..dto.authorDto import AuthorDto
from ..service.author_service import post, get_all, get, delete_all, delete

api = AuthorDto.api
_author = AuthorDto.author

@api.route('/')
class Authors(Resource):
    """Handle all authors."""
    @api.response(200, 'All authors have been listed.')
    @api.doc('List all authors.')
    @api.marshal_list_with(_author, envelope='data')
    def get(self):
        """List all authors."""
        return get_all()

    @api.response(201, 'The author has been created.')
    @api.response(409, 'The author already exists.')
    @api.doc('Create a new author.')
    @api.expect(_author, validate=True)
    def post(self):
        """Create a new author."""
        data = request.json
        return post(data=data)

    @api.response(200, 'All authors have been deleted.')
    @api.doc('Delete all authors.')
    @api.marshal_list_with(_author, envelope='data')
    def delete(self):
        """Delete all authors."""
        return delete_all()

@api.route('/<name>')
class Author(Resource):
    """Handle one author."""
    @api.response(200, 'The author has been found.')
    @api.response(404, 'The author has not been found.')
    @api.doc('Display the author with the name you are looking for.')
    @api.marshal_with(_author)
    def get(self, name):
        """Display the author with the name you are looking for."""
        author = get(name)
        if not author:
            return api.abort(404)
        return author

    @api.response(200, 'The author has been deleted.')
    @api.response(404, 'The author has not been found.')
    @api.doc('Delete the author with the name you are looking for.')
    @api.marshal_with(_author)
    def delete(self, name):
        """Delete the author with the name you are looking for."""
        author = self.get(name)
        delete(name)
        return author
