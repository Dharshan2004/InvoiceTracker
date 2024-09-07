from flask import Flask, render_template
from .main import main as main_blueprint

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    app.register_error_handler(404, page_not_found)
    return app


