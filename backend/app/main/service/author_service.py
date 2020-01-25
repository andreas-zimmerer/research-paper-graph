"""Author Service"""
from app.main import db
from app.main.model.author import Author

def post(data):
    """Create a new author."""
    author = Author.query.filter_by(id=data['id']).first()
    if author:
        response = {
            'status': 'Failure',
            'message': 'The author already exists.'
        }
        return response, 409
    author = Author(id=data['id'], name=data['name'])
    save_changes(author)
    response = {
        'status': 'Success',
        'message': 'The author has been created.'
    }
    return response, 201

def delete(name):
    """Delete the author with the name you are looking for."""
    Author.query.filter_by(name=name).delete()
    db.session.commit()

def delete_all():
    """Delete all authors."""
    Author.query.delete()
    db.session.commit()

def get_all():
    """List all authors."""
    return Author.query.all()

def get(name):
    """Display the author with the name you are looking for."""
    return Author.query.filter_by(name=name).first()

def save_changes(data):
    """Save to database"""
    db.session.add(data)
    db.session.commit()
