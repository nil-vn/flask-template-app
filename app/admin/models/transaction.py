from datetime import datetime
from typing import Optional

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.utils import db
from .base import BaseModel
from .transaction_car import transaction_car


class Transaction(BaseModel):
    __tablename__ = "transaction"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    purchase_time: Mapped[Optional[str]]
    selling_price: Mapped[Optional[float]]
    status: Mapped[Optional[str]]
    note: Mapped[Optional[str]]
    created_at: Mapped[str] = mapped_column(default=datetime.utcnow)

    customer_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("customer.id", ondelete="CASCADE"), nullable=True
    )

    # Quan hệ với Customer
    customer = relationship("Customer", back_populates="transactions")

    # Quan hệ nhiều-nhiều với Car
    cars = relationship("Car", secondary=transaction_car, back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.name}>"

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