from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Property(db.Model):
    """ Property Model for storing properties related details """
    __tablename__ = "property"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    property_type = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    rooms_count = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "<Property '{}'>".format(self.name)