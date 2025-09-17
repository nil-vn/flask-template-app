import os

import jsonify
from flask import render_template, jsonify


from flask import Blueprint

routes = Blueprint("homepage_api_routes", __name__, url_prefix="/api")


@routes.route("/test_home", methods=["GET"])
def test_home():
    return jsonify({"status": "OK"}), 200
