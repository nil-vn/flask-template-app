import os

from app import create_app
from app.utils.constants import ENV

env = os.environ.get(ENV.INIT.value, ENV.PRODUCTION.value)  # default is production

_app = create_app(f"config.{env}.{env.capitalize()}Config")


if __name__ == "__main__":
    _app.run(debug=True)
