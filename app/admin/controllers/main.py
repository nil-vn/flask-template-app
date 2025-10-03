from types import SimpleNamespace

from flask import redirect
from flask import flash, url_for

from app.admin.models import User, Customer
from app.admin.services.forms import (
    RegisterForm,
)
from app.utils.db import db
from werkzeug.security import generate_password_hash

from flask import render_template
from flask_login import login_required
from . import routes
from ..services.analytics import get_metrics


@routes.route("/")
@routes.route("/dashboard")
@login_required
def dashboard():
    metric = get_metrics()
    return render_template("dashboard.html", metric=metric)
