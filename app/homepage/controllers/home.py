from app.homepage import routes
from flask import render_template


@routes.route('/')
def index():
    return render_template('index.html')