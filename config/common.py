import os
from datetime import timedelta

basedir = os.getcwd()


class Config(object):
    SECRET_KEY = "ee2e67ea1cd3b467e1e571e71b296e13"
    PORT = 80
    BABEL_DEFAULT_LOCALE = "en"
    CREATE_ENGINE_PARAMS = {"timeout": 60 * 5}
    BASE_DIR = basedir
    APP_DB_FILE = os.path.join(basedir, "instance", "db.sqlite3")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + APP_DB_FILE
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
