"""Database model for references"""
from .. import db

class Reference(db.Model): # pylint: disable=too-few-public-methods
    """ Reference Model for storing reference related details """
    __tablename__ = "reference"

    id = db.Column(db.Integer, primary_key=True) # pylint: disable=no-member
    from_paper = db.Column(db.String(42)) # pylint: disable=no-member
    to_paper = db.Column(db.String(42)) # pylint: disable=no-member
