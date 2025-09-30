from flask import render_template

import os

from flask import Blueprint

from app.utils import login_manager

routes = Blueprint(
    "homepage_routes",
    __name__,
    template_folder=os.path.join("..", "..", "..", "templates", "homepage"),
    static_folder=os.path.join("..", "..", "..", "static", "homepage"),
    url_prefix="/",
)


@routes.route("/")
def index():
    return render_template("homepage_index.html")
