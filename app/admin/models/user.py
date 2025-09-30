from flask_login import UserMixin

# Other modules
from datetime import datetime

from app.admin.models.base import BaseModel
from app.utils import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, UserMixin):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.name}>"

    @classmethod
    def field_names(cls):
        """Return all column names for this model."""
        return [c.name for c in cls.__table__.columns]

    @classmethod
    def from_form(cls, form):
        """Create instance from a form, filtering only valid fields."""
        data = {k: v for k, v in form.data.items() if k in cls.field_names()}
        return cls(**data)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find(cls, username, email):
        return cls.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
