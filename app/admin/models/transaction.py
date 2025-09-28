from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.admin.models import Customer, Car
from app.utils import db


class Transaction(db.Model):
    __tablename__ = "transaction"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    purchase_time: Mapped[Optional[str]]
    selling_price: Mapped[Optional[float]]
    status: Mapped[Optional[str]]
    note: Mapped[Optional[str]]
    created_at: Mapped[str] = mapped_column(default=datetime.utcnow)

    car_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("car.id", ondelete="CASCADE"), nullable=True
    )
    cars: Mapped["Car"] = relationship(back_populates="transactions")
    customer_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("customer.id", ondelete="CASCADE"), nullable=True
    )
    customer: Mapped["Customer"] = relationship(back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.name}>"
