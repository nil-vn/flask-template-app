# Other modules
from datetime import datetime

from app.utils import db


class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    key = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=True)
