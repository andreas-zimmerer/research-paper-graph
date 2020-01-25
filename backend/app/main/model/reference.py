"""Reference Model"""
from .. import db

class Reference(db.Model):
    """Reference Model"""
    __tablename__ = "reference"

    id = db.Column(db.Integer, primary_key=True)
    from_paper = db.Column(db.String(42))
    to_paper = db.Column(db.String(42))
