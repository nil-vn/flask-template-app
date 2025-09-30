import logging
import os
from flask import Blueprint, request, redirect
from flask import render_template, flash, url_for

from app.admin.models import User, Transaction, Car, Customer
from app.admin.services.forms import (
    LoginForm,
)
from app.utils import login_manager
from flask_login import login_user, logout_user, login_required, current_user

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
                flash(f"{err_code}: {e}", "danger")
    return render_template("login.html", form=form)


@routes.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("admin_routes.login"))


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


# import route handlers
from .main import *
from .car import *
from .customer import *
from .transaction import *
from .user import *
