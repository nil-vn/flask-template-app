from typing import Optional, Union

from flask import Flask, request, render_template
from flask_babel import Babel


def create_app(env: Optional[Union[str, object]]) -> Flask:
    # Initialize app
    _app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/",
    )

    _app.config.from_object(env)

    # Initialize extensions
    from app.utils import db, csrf, bcrypt, login_manager

    db.init_app(_app)
    csrf.init_app(_app)
    bcrypt.init_app(_app)
    login_manager.init_app(_app)
    login_manager.login_view = "admin_routes.login"  # redirect nếu chưa login

    def get_locale():
        return request.cookies.get("locale") or _app.config["BABEL_DEFAULT_LOCALE"]

    Babel(_app, locale_selector=get_locale)

    # Create database tables
    import app.admin.models
    import app.homepage.models

    with _app.app_context():
        db.create_all()

    # Register blueprints
    from app.admin import Admin
    from app.homepage import Homepage

    Admin(_app).register()
    Homepage(_app).register()

    # error handler
    @_app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template("404.html"), 404

    @_app.errorhandler(500)
    def internal_server_error(e):
        return render_template("404.html"), 500

    return _app
