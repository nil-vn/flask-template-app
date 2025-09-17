from typing import Optional, Union

from flask import Flask


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

    return _app
