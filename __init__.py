from flask import Flask
from app.controllers.sort_controller import sort_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(sort_bp, url_prefix='/api/sort')

    return app