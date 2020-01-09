"""Database service for references"""
from app.main import db
from app.main.model.reference import Reference

def post(data):
    """Create a new reference."""
    source = data['from_paper']
    sink = data['to_paper']
    reference = Reference.query.filter_by(from_paper=source).filter_by(to_paper=sink).first()
    if reference:
        response = {
            'status': 'Failure',
            'message': 'The reference already exists.'
        }
        return response, 409

    reference = Reference(from_paper=source, to_paper=sink)
    save_changes(reference)
    response = {
        'status': 'Success',
        'message': 'The reference has been created.'
    }
    return response, 201

def delete_all():
    """Delete all references."""
    Reference.query.delete()
    db.session.commit()

def get_all():
    """List all references."""
    return Reference.query.all()

def delete(source, sink):
    """Delete the reference you are looking for."""
    Reference.query.filter_by(from_paper=source).filter_by(to_paper=sink).delete()
    db.session.commit()

def get(source, sink):
    """Display the reference you are looking for."""
    print('Hello %s', source)
    return Reference.query.filter_by(from_paper=source).filter_by(to_paper=sink).first()

def save_changes(data):
    """Save to database"""
    db.session.add(data)
    db.session.commit()
