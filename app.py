from flask import Flask, jsonify
from flask_cors import CORS
from app.controllers.sort_controller import sort_bp
from app.controllers.user_controller import user_bp
from app.controllers.simulation_controller import sim_bp
from app.config.config import Config
from app.database.db import db
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

app.register_blueprint(sort_bp, url_prefix='/api/sort')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(sim_bp, url_prefix='/api/simulations')

@app.route('/')
def home():
    return jsonify({"message": "Backend Sort API is running"})

if __name__ == '__main__':
   
    app.run(debug=True)