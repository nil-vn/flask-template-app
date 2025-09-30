from flask import request, redirect
from flask import render_template, flash, url_for

from app.admin.models import Car, Customer, Transaction
from app.admin.services.create_or_updating import create_transaction_from_form
from app.admin.services.forms import (
    TransactionForm,
)
from app.utils.db import db
from flask_login import login_required
from . import routes


@routes.route("/transactions")
@login_required
def transactions():
    all_transactions = Transaction.get_all()
    return render_template("transactions.html", transactions=all_transactions)


@routes.route("/transaction/new", methods=["GET", "POST"])
@login_required
def transaction_new():
    form = TransactionForm()
    customer_id = request.args.get("customer_id")
    car_id = request.args.get("car_id")

    # Prefill nếu có từ query param
    if customer_id:
        form.customer_id.data = customer_id
    if car_id:
        form.car_id.data = car_id

    if request.method == "POST" and form.validate_on_submit():
        try:
            create_transaction_from_form(form)
            flash("Transaction created successfully!", "success")
            return redirect(url_for("admin_routes.transactions"))
        except Exception as e:
            flash(f"Error creating transaction: {e}", "danger")

    cars = Car.get_all()
    customers = Customer.get_all()
    return render_template(
        "transaction_new.html", cars=cars, customers=customers, form=form
    )


@routes.route("/transaction/<transaction_id>", methods=["GET", "POST"])
@login_required
def transaction_detail(transaction_id):
    form = TransactionForm()
    transaction = Transaction.get_by_id(transaction_id)
    if not transaction:
        flash("Transaction not found.", "danger")
        return render_template("404.html"), 404

    if request.method == "POST":
        form = TransactionForm(obj=transaction)
        if form.validate_on_submit():
            try:
                form.populate_obj(transaction)
                db.session.commit()
                flash("Transaction updated successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error updating transaction: {e}", "danger")
    customers = Customer.get_all()
    cars = Car.get_all()
    return render_template(
        "transaction_detail.html",
        transaction=transaction,
        form=form,
        customers=customers,
        cars=cars,
    )


@routes.route("/transaction/<int:transaction_id>/delete", methods=["GET"])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.get_by_id(transaction_id)
    if not transaction:
        flash("Transaction not found.", "danger")
        return redirect(url_for("admin_routes.transactions"))

    try:
        db.session.delete(transaction)
        db.session.commit()
        flash("Transaction deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()  # rollback nếu lỗi
        flash(f"Error deleting transaction: {e}", "danger")

    return redirect(url_for("admin_routes.transactions"))
