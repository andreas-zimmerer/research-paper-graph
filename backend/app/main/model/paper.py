"""Database model for papers"""
from .. import db

class Paper(db.Model): # pylint: disable=too-few-public-methods
    """ Paper Model for storing paper related details """
    __tablename__ = "paper"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    year = (db.Integer)
    abstract = db.Column(db.String(255), nullable=False)
