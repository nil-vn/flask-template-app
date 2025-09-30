import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logger(app):
    # --- setup logging global ---
    log_dir = os.path.join("log")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d") + ".log")

    handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    handler.suffix = "%Y-%m-%d"
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)

    # Handler ghi console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)


    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)
    root_logger.addHandler(console_handler)

    # cũng add cho Flask app
    app.logger.handlers = root_logger.handlers
    app.logger.setLevel(log_level)