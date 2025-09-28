from datetime import datetime
from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)


from app.utils.db import db


class Car(db.Model):
    __tablename__ = "car"
    __table_args__ = {"sqlite_autoincrement": True}
    __except__cols = ["customer"]

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    branch: Mapped[Optional[str]]
    model: Mapped[Optional[str]]
    vin: Mapped[Optional[str]]
    color: Mapped[Optional[str]]
    traded_company: Mapped[Optional[str]]
    imported_date: Mapped[Optional[str]]
    inspection_from: Mapped[Optional[str]]
    inspection_to: Mapped[Optional[str]]
    year_of_manufacture: Mapped[Optional[str]]
    purchase_price: Mapped[Optional[float]]
    expected_selling_price: Mapped[Optional[int]]
    actual_selling_price: Mapped[Optional[int]]
    status: Mapped[Optional[str]]
    note: Mapped[Optional[str]]
    license_plate_no: Mapped[Optional[str]]

    customer_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("customer.id", ondelete="CASCADE"), nullable=True
    )
    customer: Mapped["Customer"] = relationship(back_populates="cars")
    transaction_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("transaction.id", ondelete="CASCADE"), nullable=True
    )
    transactions: Mapped["Transaction"] = relationship(back_populates="cars")

    created_at: Mapped[str] = mapped_column(default=datetime.utcnow)

    def __repr__(self):
        return f"<Car {self.name}>"

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
    def get_by_status(cls, status):
        return cls.query.filter(cls.status == status).all()

    @classmethod
    def get_by_id(cls, qid):
        return cls.query.get(qid)
