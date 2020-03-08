"""Paper Model"""
from .. import db

class Paper(db.Model):
    """Paper Model"""
    __tablename__ = "paper"

    id = db.Column(db.String(42), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    abstract = db.Column(db.Text, nullable=False)
    citations = db.Column(db.Integer)
