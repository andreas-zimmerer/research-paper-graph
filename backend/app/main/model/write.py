"""Write Model"""
from .. import db

class Write(db.Model):
    """Write Model"""
    __tablename__ = "write"

    id = db.Column(db.Integer, primary_key=True)
    paper = db.Column(db.String(42))
    author = db.Column(db.String(42))
