"""Database service for references"""
from app.main import db
from app.main.model.reference import Reference

def save_new_reference(data):
    """POST reference"""
    reference = Reference.query.filter_by(from_paper=data['from_paper']).filter_by(to_paper=data['to_paper']).first()
    if not reference: # pylint: disable=no-else-return
        new_reference = Reference(
            from_paper=data['from_paper'],
            to_paper=data['to_paper']
        )
        save_changes(new_reference)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Reference already exists'
        }
        return response_object, 409

def get_all_references():
    """GET all references"""
    return Reference.query.all()

def save_changes(data):
    """Save to database"""
    db.session.add(data) # pylint: disable=no-member
    db.session.commit() # pylint: disable=no-member