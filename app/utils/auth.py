from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

bcrypt = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "routes.login"
login_manager.login_message_category = "info"
