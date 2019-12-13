from .. import db, flask_bcrypt

class Paper(db.Model):
    """ Paper Model for storing paper related details """
    __tablename__ = "paper"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    year = (db.Integer)
    abstract = db.Column(db.String(255), nullable=False)