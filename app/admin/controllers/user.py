from flask import redirect, request
from flask import render_template, flash, url_for

from app.admin.models import User
from app.admin.services.forms import (
    RegisterForm, UserUpdateForm,
)
from app.utils.db import db
from flask_login import login_required
from werkzeug.security import generate_password_hash
from . import routes, logger


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
                password_hash=password_hash,
                role=form.role.data
            )
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully!", "success")
        except Exception as e:
            db.session.rollback()
            logger.exception(e)
            flash("Could not create user", "error")
        finally:
            return redirect(url_for('admin_routes.register'))
    elif form.errors:
        for err_code, err_content in form.errors.items():
            for e in err_content:
                flash(f"{err_code}: {e}", "danger")
        return redirect(url_for('admin_routes.register'))
    return render_template("user_new.html", form=form)


@routes.route("/users")
def users():
    all_users = User.get_all()
    return render_template("users.html", users=all_users)


@routes.route("/user/<int:user_id>/delete", methods=["GET"])
@login_required
def delete_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("admin_routes.users"))

    try:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()  # rollback nếu lỗi
        flash(f"Error deleting user: {e}", "danger")

    return redirect(url_for("admin_routes.users"))

@routes.route("/user/<user_id>", methods=["GET", "POST"])
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    form = UserUpdateForm(obj=user)  # populate form với dữ liệu hiện tại

    if form.validate_on_submit():
        # Kiểm tra username/email có trùng với user khác không
        existing_user = User.query.filter(
            ((User.username == form.username.data) | (User.email == form.email.data)) &
            (User.id != user.id)
        ).first()
        if existing_user:
            flash("Username or email already exists", "danger")
            return render_template("user_detail.html", form=form, user=user)

        try:
            # Cập nhật thông tin user
            user.username = form.username.data
            user.email = form.email.data
            user.role = form.role.data

            # Nếu có nhập password mới, hash lại
            if form.password.data:
                user.password_hash = generate_password_hash(form.password.data)

            db.session.commit()
            flash("User updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            logger.exception(e)
            flash("Could not update user", "danger")
    elif form.errors:
        for field, errors in form.errors.items():
            for e in errors:
                flash(f"{field}: {e}", "danger")

    return render_template("user_detail.html", form=form, user=user)