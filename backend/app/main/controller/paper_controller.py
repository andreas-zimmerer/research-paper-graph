"""Paper Controller"""
from flask_restplus import Resource
from flask import request

from ..dto.dto import PaperDto
from ..service.paper_service import post, get_all, get, search, delete_all, delete

api = PaperDto.api
_paper = PaperDto.paper

@api.route('/')
class Papers(Resource):
    """Handle all papers."""
    @api.response(200, 'All papers have been listed.')
    @api.doc('List all papers.')
    @api.marshal_list_with(_paper, envelope='data')
    def get(self):
        """List all papers."""
        return get_all()

    @api.response(201, 'The paper has been created.')
    @api.response(409, 'The paper already exists.')
    @api.doc('Create a new paper.')
    @api.expect(_paper, validate=True)
    def post(self):
        """Create a new paper."""
        data = request.json
        return post(data=data)

    @api.response(200, 'All papers have been deleted.')
    @api.doc('Delete all papers.')
    @api.marshal_list_with(_paper, envelope='data')
    def delete(self):
        """Delete all papers."""
        return delete_all()

@api.route('/<title>')
class Paper(Resource):
    """Handle one paper."""
    @api.response(200, 'The paper has been found.')
    @api.response(404, 'The paper has not been found.')
    @api.doc('Display the paper with the title you are looking for.')
    @api.marshal_with(_paper)
    def get(self, title):
        """Display the paper with the title you are looking for."""
        paper = get(title)
        if not paper:
            return api.abort(404)
        return paper

    @api.response(200, 'The paper has been deleted.')
    @api.response(404, 'The paper has not been found.')
    @api.doc('Delete the paper with the title you are looking for.')
    @api.marshal_with(_paper)
    def delete(self, title):
        """Delete the paper with the title you are looking for."""
        paper = self.get(title)
        delete(title)
        return paper

@api.route('/search/<keyword>')
class KeywordPapers(Resource):
    """Handle all papers that contain a keyword."""
    @api.response(200, 'All papers that contain the searched keyword have been listed.')
    @api.doc('List all papers that contain a searched keyword.')
    @api.marshal_list_with(_paper)
    def get(self, keyword):
        """List all papers that contain a searched keyword."""
        return search(keyword)
