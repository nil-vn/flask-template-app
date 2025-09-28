from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import ForeignKey

from app.admin.models import Car
from app.utils import db


class Customer(db.Model):
    __tablename__ = "customer"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    gender: Mapped[Optional[str]]
    birth_day: Mapped[Optional[str]]
    facebook: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    address: Mapped[Optional[str]]
    license_img: Mapped[Optional[str]]
    gallery_id: Mapped[Optional[int]]
    lead_source: Mapped[Optional[str]]
    status: Mapped[Optional[str]]
    note: Mapped[Optional[str]]

    cars: Mapped[List["Car"]] = relationship(back_populates="customer")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="customer")

    created_at: Mapped[str] = mapped_column(default=datetime.utcnow)

    def __repr__(self):
        return f"<Customer {self.name}>"

    @classmethod
    def field_names(cls):
        """Return all column names for this model."""
        return [c.name for c in cls.__table__.columns]

    @classmethod
    def from_form(cls, form):
        """Create instance from a form, filtering only valid fields."""
        data = {k: v for k, v in form.data.items() if k in cls.field_names()}
        return cls(**data)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, qid):
        return cls.query.get(qid)
