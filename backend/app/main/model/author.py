"""Author Model"""
from .. import db

class Author(db.Model):
    """Author Model"""
    __tablename__ = "author"

    id = db.Column(db.String(42), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
