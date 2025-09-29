import os
from flask import Blueprint, request, redirect
from flask import render_template, flash, url_for

from app.admin.models import Car, Customer, Transaction
from app.admin.services.create_or_updating import create_transaction_from_form
from app.admin.services.forms import CarForm, CustomerForm, TransactionForm
from app.utils import login_manager
from app.utils.db import db
from flask_babel import gettext as _

routes = Blueprint(
    "admin_routes",
    __name__,
    template_folder=os.path.join("..", "..", "..", "templates", "admin"),
    static_folder=os.path.join("..", "..", "..", "static", "admin"),
    url_prefix="/admin",
)


@login_manager.user_loader
def load_user():
    return True


@routes.route("/")
@routes.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@routes.route("/inventory")
def inventory():
    cars = Car.get_all()
    reserved_cars = Car.get_by_status("reserved")
    available_cars = Car.get_by_status("available")
    unchecked_cars = Car.get_by_status("unchecked")
    return render_template(
        "inventory.html",
        cars=cars,
        reserved_cars=reserved_cars,
        available_cars=available_cars,
        unchecked_cars=unchecked_cars,
    )


@routes.route("/inventory/new", methods=["GET", "POST"])
def inventory_new():
    form = CarForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Add to session and commit
            new_car = Car.from_form(form)
            try:
                with db.session.begin():
                    db.session.add(new_car)
                # Nếu đến đây, commit đã thành công
                flash("Car added successfully!", "success")
            except Exception as e:
                flash(f"Error adding car: {e}", "danger")
                raise e
    return render_template("inventory_new.html", form=form)


@routes.route("/inventory/detail/<car_id>", methods=["GET", "POST"])
def car_detail(car_id):
    form = CarForm()
    car = Car.get_by_id(car_id)
    if not car:
        flash("Car not found.", "danger")
        return render_template("404.html"), 404

    if request.method == "POST":
        form = CarForm(obj=car)
        if form.validate_on_submit():
            try:
                form.populate_obj(car)
                db.session.commit()
                flash("Car updated successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error updating car: {e}", "danger")
    customers = Customer.get_all()
    return render_template("car_detail.html", car=car, form=form, customers=customers)


@routes.route("/inventory/detail/<int:car_id>/delete", methods=["GET"])
def delete_car(car_id):
    car = Car.get_by_id(car_id)
    if not customer:
        flash("Car not found.", "danger")
        return redirect(url_for("admin_routes.inventory"))

    try:
        db.session.delete(car)
        db.session.commit()
        flash("Car deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting car: {e}", "danger")

    return redirect(url_for("admin_routes.inventory"))


@routes.route("/login")
def login():
    return render_template("login.html")


@routes.route("/search")
def search():
    return render_template("search.html")


@routes.route("/customer")
def customer():
    customers = Customer.get_all()
    return render_template("customer.html", customers=customers)


@routes.route("/customer/new", methods=["GET", "POST"])
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
    return render_template("customer_detail.html", customer=customer, form=form, cars=cars)


@routes.route("/customer/<int:customer_id>/purchase/new", methods=["GET", "POST"])
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


@routes.route("/car/<int:car_id>/purchase/new", methods=["GET", "POST"])
def add_car_purchase(car_id):
    form = TransactionForm()
    customers = Customer.get_all()
    car = Car.get_by_id(car_id)
    form.car_id.data = int(car_id)  # Prefill car_id
    if request.method == "POST" and form.validate_on_submit():
        try:
            create_transaction_from_form(form)
            flash("Purchase added for car successfully!", "success")
        except Exception as e:
            flash(f"Error creating transaction: {e}", "danger")
    return redirect(url_for("admin_routes.car_detail", car_id=car.id))


@routes.route("/customer/<int:customer_id>/delete", methods=["GET"])
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


@routes.route("/transaction")
def transaction():
    transactions = Transaction.get_all()
    return render_template(
        "transaction.html",
        transactions=transactions
    )


@routes.route("/transaction/new", methods=["GET", "POST"])
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
            return redirect(url_for("admin_routes.transaction"))
        except Exception as e:
            flash(f"Error creating transaction: {e}", "danger")

    cars = Car.get_all()
    customers = Customer.get_all()
    return render_template("transaction_new.html", cars=cars, customers=customers, form=form)


@routes.route("/transaction/<transaction_id>", methods=["GET", "POST"])
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
    return render_template("transaction_detail.html", transaction=transaction, form=form)

@routes.route("/transaction/<int:transaction_id>/delete", methods=["GET"])
def delete_transaction(transaction_id):
    transaction = Transaction.get_by_id(transaction_id)
    if not transaction:
        flash("Transaction not found.", "danger")
        return redirect(url_for("admin_routes.transaction"))

    try:
        db.session.delete(transaction)
        db.session.commit()
        flash("Transaction deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()  # rollback nếu lỗi
        flash(f"Error deleting transaction: {e}", "danger")

    return redirect(url_for("admin_routes.transaction"))