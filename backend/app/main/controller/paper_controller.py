"""Database controller for papers"""
from flask_restplus import Resource
from flask import request

from ..dto.dto import PaperDto
from ..service.paper_service import save_new_paper, get_all_papers, get_a_paper, search_paper

api = PaperDto.api
_paper = PaperDto.paper

@api.route('/')
class PaperList(Resource):
    """Class for all papers"""
    @api.doc('list_of_registered_papers')
    @api.marshal_list_with(_paper, envelope='data')
    def get(self):
        """List all registered papers"""
        return get_all_papers()

    @api.response(201, 'Paper successfully created.')
    @api.doc('create a new paper')
    @api.expect(_paper, validate=True)
    def post(self):
        """Creates a new Paper"""
        data = request.json
        return save_new_paper(data=data)


@api.route('/<title>')
@api.param('title', 'The Paper title')
@api.response(404, 'Paper not found.')
class Paper(Resource):
    """Class for one paper"""
    @api.doc('get a paper')
    @api.marshal_with(_paper)
    def get(self, title):
        """get a paper given its title"""
        paper = get_a_paper(title)
        if not paper:
            return api.abort(404)
        else:
            return paper

@api.route('/search/<keyword>')
@api.param('keyword', 'The searched keyword')
class PaperSearch(Resource):
    """Class for searching papers"""
    @api.doc('search papers')
    @api.marshal_list_with(_paper)
    def get(self, keyword):
        """search papers for a keyword"""
        result = search_paper(keyword)
        return result
