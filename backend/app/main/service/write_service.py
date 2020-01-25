"""Write Service"""
from app.main import db
from app.main.model.write import Write

def post(data):
    """Create a new writing relation."""
    paper = data['paper']
    author = data['author']
    write = Write.query.filter_by(paper=paper).filter_by(author=author).first()
    if write:
        response = {
            'status': 'Failure',
            'message': 'The writing relation already exists.'
        }
        return response, 409

    write = Write(paper=paper, author=author)
    save_changes(write)
    response = {
        'status': 'Success',
        'message': 'The writing relation has been created.'
    }
    return response, 201

def delete_all():
    """Delete all writing relations."""
    Write.query.delete()
    db.session.commit()

def get_all():
    """List all writing relations."""
    return Write.query.all()

def delete(paper, author):
    """Delete the writing relation you are looking for."""
    Write.query.filter_by(paper=paper).filter_by(author=author).delete()
    db.session.commit()

def get(paper, author):
    """Display the writing relation you are looking for."""
    return Write.query.filter_by(paper=paper).filter_by(author=author).first()

def save_changes(data):
    """Save to database"""
    db.session.add(data)
    db.session.commit()
