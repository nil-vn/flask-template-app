import logging
import os
from flask import Blueprint, request, redirect
from flask import render_template, flash, url_for

from app.admin.models import Car, Customer, Transaction, User
from app.admin.services.create_or_updating import create_transaction_from_form
from app.admin.services.forms import (
    CarForm,
    CustomerForm,
    TransactionForm,
    LoginForm,
    RegisterForm,
)
from app.utils import login_manager
from app.utils.db import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

logger = logging.getLogger(__name__)

routes = Blueprint(
    "admin_routes",
    __name__,
    template_folder=os.path.join("..", "..", "..", "templates", "admin"),
    static_folder=os.path.join("..", "..", "..", "static", "admin"),
    url_prefix="/admin",
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@routes.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_routes.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # <-- dùng Flask-Login
            flash("Logged in successfully!", "success")
            next_url = request.args.get("next") or url_for("admin_routes.dashboard")
            return redirect(next_url)
        else:
            flash("Invalid username or password", "danger")
    elif form.errors:
        for err_code, err_content in form.errors.items():
            for e in err_content:
                flash(f'{err_code}: {e}', "danger")
    return render_template("login.html", form=form)


@routes.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("admin_routes.login"))


@routes.route("/")
@routes.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@routes.route("/cars")
@login_required
def cars():
    all_cars = Car.get_all()
    reserved_cars = Car.get_by_status("reserved")
    available_cars = Car.get_by_status("available")
    unchecked_cars = Car.get_by_status("unchecked")
    return render_template(
        "cars.html",
        cars=all_cars,
        reserved_cars=reserved_cars,
        available_cars=available_cars,
        unchecked_cars=unchecked_cars,
    )


@routes.route("/car/new", methods=["GET", "POST"])
@login_required
def car_new():
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
    return render_template("car_new.html", form=form)


@routes.route("/car/<car_id>", methods=["GET", "POST"])
@login_required
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


@routes.route("/car/<int:car_id>/delete", methods=["GET"])
@login_required
def delete_car(car_id):
    car = Car.get_by_id(car_id)
    if not car:
        flash("Car not found.", "danger")
        return redirect(url_for("admin_routes.cars"))

    try:
        db.session.delete(car)
        db.session.commit()
        flash("Car deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting car: {e}", "danger")

    return redirect(url_for("admin_routes.cars"))


@routes.route("/search", methods=["GET", "POST"])
@login_required
def search():
    query = request.args.get("q", "").strip()
    customers, cars, transactions = [], [], []

    if query:
        # Search Customers
        customers = Customer.search(query)

        # Search Cars
        cars = Car.search(query)

        # Search Transactions
        transactions = Transaction.search(query)

    return render_template(
        "search.html",
        query=query,
        customers=customers,
        cars=cars,
        transactions=transactions,
    )


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


@routes.route("/car/<int:car_id>/purchase/new", methods=["GET", "POST"])
@login_required
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


@routes.route("/user/new", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # Check if username/email đã tồn tại
        existing_user = User.find(username=form.username.data, email=form.email.data)
        if existing_user:
            flash("Username or email already exists", "danger")
            return render_template("user_new.html", form=form)

        try:
            password_hash = generate_password_hash(form.password.data)

            # Tạo user mới
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=password_hash
            )
            db.session.add(user)
            db.session.commit()
            # Login luôn sau khi tạo account
            login_user(user)
            flash("Account created successfully!", "success")
        except Exception as e:
            db.session.rollback()
            logger.exception(e)
            flash("Could not create user", "error")
    elif form.errors:
        for err_code, err_content in form.errors.items():
            for e in err_content:
                flash(f'{err_code}: {e}', "danger")
    return render_template("user_new.html", form=form)
