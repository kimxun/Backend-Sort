from flask import Flask
from app.controllers.sort_controller import sort_bp
from app.controllers.user_controller import user_bp
from app.controllers.simulation_controller import sim_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(sort_bp, url_prefix='/api/sort')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(sim_bp, url_prefix='/api/simulations')

    return app