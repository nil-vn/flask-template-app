from flask import request, redirect
from flask import render_template, flash, url_for

from app.admin.models import Car, Customer
from app.admin.services.forms import (
    CarForm,
    TransactionForm,
)
from app.utils.db import db
from flask_login import login_required
from . import routes
from ..services.create_or_updating import create_transaction_from_form
from ...utils.constants import CarStatus, CarBranches, CarSituation


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
    car_status = CarStatus
    car_branches = CarBranches
    car_situation = CarSituation
    if request.method == "POST":
        if form.validate_on_submit():
            # Add to session and commit
            new_car = Car.from_form(form)
            try:
                db.session.add(new_car)
                db.session.commit()
                # Nếu đến đây, commit đã thành công
                flash("Car added successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error adding car: {e}", "danger")
            finally:
                return redirect(url_for('admin_routes.car_new'))
        elif form.errors:
            for err_code, err_content in form.errors.items():
                for e in err_content:
                    flash(f"{err_code}: {e}", "danger")
            return redirect(url_for('admin_routes.car_new'))
    return render_template(
        "car_new.html",
        form=form,
        car_status=car_status,
        car_branches=car_branches,
        car_situation=car_situation
    )


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
            finally:
                return redirect(url_for('admin_routes.car_detail', car_id=car_id))
        elif form.errors:
            for err_code, err_content in form.errors.items():
                for e in err_content:
                    flash(f"{err_code}: {e}", "danger")
            return redirect(url_for('admin_routes.car_detail', car_id=car_id))
    customers = Customer.get_all()
    car_status = CarStatus
    car_branches = CarBranches
    car_situation = CarSituation
    return render_template(
        "car_detail.html",
        car=car,
        form=form,
        customers=customers,
        car_status=car_status,
        car_branches=car_branches,
        car_situation=car_situation
    )


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


@routes.route("/car/<int:car_id>/purchase/new", methods=["GET", "POST"])
@login_required
def add_car_purchase(car_id):
    form = TransactionForm()
    customers = Customer.get_all()
    car = Car.get_by_id(car_id)
    form.car_id.data = int(car_id)  # Prefill car_id
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                create_transaction_from_form(form)
                flash("Purchase added for car successfully!", "success")
            except Exception as e:
                flash(f"Error creating transaction: {e}", "danger")
        elif form.errors:
            for err_code, err_content in form.errors.items():
                for e in err_content:
                    flash(f"{err_code}: {e}", "danger")
    return redirect(url_for("admin_routes.car_detail", car_id=car.id))
