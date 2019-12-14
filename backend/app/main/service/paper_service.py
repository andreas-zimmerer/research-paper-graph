import uuid
import datetime

from app.main import db
from app.main.model.paper import Paper

def save_new_paper(data):
    paper = Paper.query.filter_by(title=data['title']).first()
    if not paper:
        new_paper = Paper(
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
    return Paper.query.all()

def get_a_paper(title):
    return Paper.query.filter_by(title=title).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()