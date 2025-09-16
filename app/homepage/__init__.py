import os

from flask import Blueprint

routes = Blueprint(
    "homepage_routes",
    __name__,
    template_folder=os.path.join('..', '..', 'templates', 'homepage'),
    static_folder=os.path.join('..', '..', 'static', 'homepage'),
    url_prefix="/")
