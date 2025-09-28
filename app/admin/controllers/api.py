import os

import jsonify
from flask import render_template, jsonify


from flask import Blueprint, request

from app.admin.services.forms import CarForm

routes = Blueprint("admin_api_routes", __name__, url_prefix="/api")


@routes.route("/test_admin", methods=["GET"])
def test_api():
    return jsonify({"status": "OK"}), 200
