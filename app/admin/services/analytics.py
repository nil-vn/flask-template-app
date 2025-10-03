from datetime import datetime
from types import SimpleNamespace

from app.admin.models import Customer, Transaction, Car


def get_all_customers():
    customers = Customer.get_all()
    return customers

def get_recently_count(model):
    now = datetime.utcnow()
    # tháng hiện tại
    start_current_month = datetime(now.year, now.month, 1)
    # tháng trước
    if now.month == 1:
        start_prev_month = datetime(now.year - 1, 12, 1)
    else:
        start_prev_month = datetime(now.year, now.month - 1, 1)

    # số user tháng hiện tại
    current_count = model.current_count(start_current_month)

    # số user tháng trước
    prev_count = model.prev_count(start_current_month, start_prev_month)

    # tính % tăng trưởng
    growth_rate = 0
    if prev_count > 0:
        growth_rate = ((current_count - prev_count) / prev_count) * 100

    return SimpleNamespace(
        total=current_count,
        monthly_increase=round(growth_rate, 2)
    )


def get_metrics():
    return SimpleNamespace(
        customers=get_recently_count(Customer),
        transactions=get_recently_count(Transaction),
        cars=get_recently_count(Car)
    )