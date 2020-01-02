"""Database service for papers"""
from app.main import db
from app.main.model.paper import Paper

def post(data):
    """Create a new paper."""
    paper = Paper.query.filter_by(id=data['id']).first()
    if paper:
        response = {
            'status': 'Failure',
            'message': 'The paper already exists.'
        }
        return response, 409
    paper = Paper(id=data['id'], title=data['title'], year=data['year'], abstract=data['abstract'])
    save_changes(paper)
    response = {
        'status': 'Success',
        'message': 'The paper has been created.'
    }
    return response, 201

def delete(title):
    """Delete the paper with the title you are looking for."""
    Paper.query.filter_by(title=title).delete()
    db.session.commit()

def get_all():
    """List all papers."""
    return Paper.query.all()

def get(title):
    """Display the paper with the title you are looking for."""
    return Paper.query.filter_by(title=title).first()

def search(keyword):
    """List all papers that contain a searched keyword."""
    return Paper.query.filter(Paper.title.like(f"%{keyword}%")).all()

def save_changes(data):
    """Save to database"""
    db.session.add(data)
    db.session.commit()
