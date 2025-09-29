from app.admin.models import Transaction, Car, Customer
from app.utils import db


# Service function tái sử dụng
def create_transaction_from_form(form):
    """Tạo transaction mới từ form."""
    new_transaction = Transaction.from_form(form)
    car_id = int(form.car_id.data) if form.car_id.data else None
    customer_id = int(form.customer_id.data) if form.customer_id.data else None
    # Gắn Car
    if car_id:
        car = Car.get_by_id(car_id)
        new_transaction.cars.append(car)

    # Gắn Customer
    if customer_id:
        customer = Customer.get_by_id(customer_id)
        new_transaction.customer = customer
    db.session.add(new_transaction)
    db.session.commit()
    return new_transaction
