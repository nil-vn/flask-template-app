from abc import abstractmethod

from app.utils.register import Module
from flask import Flask


class Homepage(Module):
    def __init__(self, flask_app: Flask):
        self.flask_app = flask_app

    def register(self):
        from app.homepage.controllers.main import routes as homepage_routes
        from app.homepage.controllers.api import routes as api_routes

        self.flask_app.register_blueprint(homepage_routes)
        self.flask_app.register_blueprint(api_routes)
