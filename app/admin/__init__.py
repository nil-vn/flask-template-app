from abc import abstractmethod

from app.utils.register import Module
from flask import Flask


class Admin(Module):
    def __init__(self, flask_app: Flask):
        self.flask_app = flask_app

    def register(self):
        from app.admin.controllers import routes as admin_routes
        from app.admin.controllers.api import routes as api_routes

        self.flask_app.register_blueprint(admin_routes)
        self.flask_app.register_blueprint(api_routes)
