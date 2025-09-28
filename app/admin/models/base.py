from app.utils.db import db

class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def field_names(cls):
        """Return all column names for this model."""
        return [c.name for c in cls.__table__.columns]

    @classmethod
    def from_form(cls, form):
        """Create instance from a form, filtering only valid fields."""
        data = {k: v for k, v in form.data.items() if k in cls.field_names()}
        return cls(**data)


class Configuration(BaseModel):
    __tablename__ = "config"
    __table_args__ = {"sqlite_autoincrement": True}

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    key = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=True)
