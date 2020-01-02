"""Database service for papers"""
from app.main import db
from app.main.model.paper import Paper

def save_new_paper(data):
    """POST paper"""
    paper = Paper.query.filter_by(id=data['id']).first()
    if not paper:
        new_paper = Paper(
            id=data['id'],
            title=data['title'],
            year=data['year'],
            abstract=data['abstract']
        )
        save_changes(new_paper)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Paper already exists'
        }
        return response_object, 409

def get_all_papers():
    """GET all papers"""
    return Paper.query.all()

def get_a_paper(title):
    """GET paper by title"""
    return Paper.query.filter_by(title=title).first()

def search_paper(keyword):
    """SEARCH paper by keyword"""
    return Paper.query.filter(Paper.title.like(f"%{keyword}%")).all()

def save_changes(data):
    """Save to database"""
    db.session.add(data)
    db.session.commit()