from app.utils import db

transaction_car = db.Table(
    "transaction_car",
    db.Column(
        "transaction_id", db.Integer, db.ForeignKey("transaction.id"), primary_key=True
    ),
    db.Column("car_id", db.Integer, db.ForeignKey("car.id"), primary_key=True),
)
