from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from app.controllers.sort_controller import sort_bp
from app.controllers.user_controller import user_bp
from app.controllers.simulation_controller import sim_bp
from app.config.config import Config
from app.database.db import db
from app.controllers.algorithm_controller import algorithm_bp
from app.controllers.auth_controller import auth_bp
from app.models.algorithm import Algorithm
from app.models.algorithm_category import AlgorithmCategory
from app.models.simulation_history import SimulationHistory
from app.models.user import User
from app.config.cache import cache
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config.from_object(Config)
print(app.config["SMTP_USER"])
print(app.config["SMTP_PASSWORD"])
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
cache.init_app(app)

app.config['SWAGGER'] = {
    'swagger': '2.0',
    'title': 'Backend Sort API',
    'version': '1.0',
    'description': 'API quản lý thuật toán sắp xếp, người dùng, xác thực JWT',
    'securityDefinitions': {
        'BearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'security': [{'BearerAuth': []}]        
}
swagger = Swagger(app)

db.init_app(app)

CORS(app, origins="*", allow_headers=["Authorization", "Content-Type", "Accept", "X-Guest-ID"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

app.register_blueprint(sort_bp, url_prefix='/api/sort')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(sim_bp, url_prefix='/api/simulations')
app.register_blueprint(algorithm_bp, url_prefix='/api/algorithms')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def home():
    return jsonify({"message": "Backend Sort API is running"})


if __name__ == '__main__':
    print("Swagger: http://127.0.0.1:5000/apidocs/")
    app.run(debug=True, use_reloader=False)