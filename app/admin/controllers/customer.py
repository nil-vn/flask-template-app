from flask import request, redirect
from flask import render_template, flash, url_for

from app.admin.models import Car, Customer
from app.admin.services.create_or_updating import create_transaction_from_form
from app.admin.services.forms import (
    CustomerForm,
    TransactionForm,
)
from app.utils.db import db
from flask_login import login_required
from . import routes


@routes.route("/customers")
@login_required
def customers():
    all_customers = Customer.get_all()
    return render_template("customers.html", customers=all_customers)


@routes.route("/customer/new", methods=["GET", "POST"])
@login_required
def customer_new():
    form = CustomerForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Add to session and commit
            new_customer = Customer.from_form(form)
            try:
                with db.session.begin():
                    db.session.add(new_customer)
                flash("Customer added successfully!", "success")
            except Exception as e:
                flash(f"Error adding car: {e}", "danger")
                raise e
    return render_template("customer_new.html", form=form)


@routes.route("/customer/<int:customer_id>", methods=["GET", "POST"])
@login_required
def customer_detail(customer_id):
    form = CustomerForm()
    customer = Customer.get_by_id(customer_id)
    if not customer:
        flash("Customer not found.", "danger")
        return render_template("404.html"), 404

    if request.method == "POST":
        form = CustomerForm(obj=customer)
        if form.validate_on_submit():
            try:
                form.populate_obj(customer)
                db.session.commit()
                flash("Customer updated successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error updating Customer: {e}", "danger")
    cars = Car.get_all()
    return render_template(
        "customer_detail.html", customer=customer, form=form, cars=cars
    )


@routes.route("/customer/<int:customer_id>/purchase/new", methods=["GET", "POST"])
@login_required
def add_customer_purchase(customer_id):
    form = TransactionForm()
    form.customer_id.data = int(customer_id)
    # Prefill customer_id
    if request.method == "POST" and form.validate_on_submit():
        try:
            create_transaction_from_form(form)
            flash("Purchase added for customer successfully!", "success")
        except Exception as e:
            flash(f"Error creating transaction: {e}", "danger")
    return redirect(url_for("admin_routes.customer_detail", customer_id=customer_id))


@routes.route("/customer/<int:customer_id>/delete", methods=["GET"])
@login_required
def delete_customer(customer_id):
    customer = Customer.get_by_id(customer_id)
    if not customer:
        flash("Customer not found.", "danger")
        return redirect(url_for("admin_routes.customer"))

    try:
        db.session.delete(customer)
        db.session.commit()
        flash("Customer deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()  # rollback nếu lỗi
        flash(f"Error deleting car: {e}", "danger")

    return redirect(url_for("admin_routes.customer"))
