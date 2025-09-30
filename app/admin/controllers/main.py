from flask import redirect
from flask import flash, url_for

from app.admin.models import User
from app.admin.services.forms import (
    RegisterForm,
)
from app.utils.db import db
from werkzeug.security import generate_password_hash

from flask import render_template
from flask_login import login_required
from . import routes


@routes.route("/")
@routes.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
