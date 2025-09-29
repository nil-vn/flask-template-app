from datetime import datetime
from typing import Optional

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy.orm import relationship
from app.utils import db
from .base import BaseModel
from .transaction_car import transaction_car
from sqlalchemy import or_


class Car(BaseModel):
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

    # Nhiều transaction qua bảng trung gian
    transactions = relationship(
        "Transaction", secondary=transaction_car, back_populates="cars"
    )

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

    @classmethod
    def search(cls, query):
        return cls.query.filter(
            or_(
                cls.name.ilike(f"%{query}%"),
                cls.vin.ilike(f"%{query}%"),
                cls.branch.ilike(f"%{query}%"),
                cls.model.ilike(f"%{query}%"),
                cls.color.ilike(f"%{query}%"),
                cls.year_of_manufacture.ilike(f"%{query}%"),
                Car.note.ilike(f"%{query}%")
            )
        ).all()