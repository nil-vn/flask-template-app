import os
from flask import Blueprint, request, redirect
from flask import render_template, flash, url_for

from app.admin.models import Car, Customer
from app.admin.services.forms import CarForm, CustomerForm
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
    return render_template(
        "car_detail.html",
        car=car,
        form=form,
        customers=customers
    )


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


@routes.route("/customer/detail/<int:customer_id>", methods=["GET", "POST"])
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
    return render_template("customer_detail.html", customer=customer, form=form)


@routes.route("/customer/detail/<int:customer_id>/delete", methods=["GET"])
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
    cars = Car.get_all()
    reserved_cars = Car.get_by_status("reserved")
    available_cars = Car.get_by_status("available")
    unchecked_cars = Car.get_by_status("unchecked")
    return render_template(
        "transaction.html",
        cars=cars,
        reserved_cars=reserved_cars,
        available_cars=available_cars,
        unchecked_cars=unchecked_cars,
    )


@routes.route("/transaction/new", methods=["GET", "POST"])
def transaction_new():
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


@routes.route("/transaction/detail/<car_id>", methods=["GET", "POST"])
def transaction_detail(car_id):
    car = Car.get_by_id(car_id)
    return render_template("transaction_detail.html", car=car)
