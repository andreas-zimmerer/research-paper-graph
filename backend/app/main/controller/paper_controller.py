from flask import request
from flask_restplus import Resource

from ..util.dto import PaperDto
from ..service.paper_service import save_new_paper, get_all_papers, get_a_paper

api = PaperDto.api
_paper = PaperDto.paper

@api.route('/')
class PaperList(Resource):
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
    @api.doc('get a paper')
    @api.marshal_with(_paper)
    def get(self, title):
        """get a paper given its title"""
        paper = get_a_paper(title)
        if not paper:
            api.abort(404)
        else:
            return paper
