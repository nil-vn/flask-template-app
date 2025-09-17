import os
from flask import render_template

from flask import Blueprint

from app.utils import login_manager

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
def index():
    return render_template("admin_index.html")
