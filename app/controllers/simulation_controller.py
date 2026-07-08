from flask import request, jsonify, Blueprint
from flasgger import swag_from
from app.repositories.simulation_history_repository import SimulationHistoryRepository
from app.utils.auth_decorator import jwt_required, roles_required

sim_bp = Blueprint('simulation', __name__, url_prefix='/simulations')

@sim_bp.route('', methods=['GET'])
@jwt_required
@roles_required(1)
@swag_from('../apidocs/simulation_get_all.yml')
def get_all_simulations():
    sims = SimulationHistoryRepository.get_all()
    return jsonify([s.to_dict() for s in sims]), 200

@sim_bp.route('/<int:sim_id>', methods=['GET'])
@jwt_required
@swag_from('../apidocs/simulation_get_one.yml')
def get_simulation(sim_id):
    sim = SimulationHistoryRepository.get_by_id(sim_id)
    if not sim:
        return jsonify({"error": "Simulation not found"}), 404
    return jsonify(sim.to_dict()), 200

@sim_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required
@swag_from('../apidocs/simulation_get_by_user.yml')
def get_simulations_by_user(user_id):
    sims = SimulationHistoryRepository.get_by_user(user_id)
    return jsonify([s.to_dict() for s in sims]), 200

@sim_bp.route('', methods=['POST'])
@jwt_required
@swag_from('../apidocs/simulation_create.yml')
def create_simulation():
    data = request.get_json()
    required = ['user_id', 'algorithm_id', 'input_data', 'sorted_result']
    if not all(k in data for k in required):
        return jsonify({"error": f"Missing fields, required: {required}"}), 400
    try:
        sim = SimulationHistoryRepository.create(data)
        return jsonify(sim.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@sim_bp.route('/<int:sim_id>', methods=['PUT'])
@jwt_required
@swag_from('../apidocs/simulation_update.yml')
def update_simulation(sim_id):
    data = request.get_json()
    sim = SimulationHistoryRepository.update(sim_id, data)
    if not sim:
        return jsonify({"error": "Simulation not found"}), 404
    return jsonify(sim.to_dict()), 200

@sim_bp.route('/<int:sim_id>', methods=['DELETE'])
@jwt_required
@roles_required(1)
@swag_from('../apidocs/simulation_delete.yml')
def delete_simulation(sim_id):
    success = SimulationHistoryRepository.delete(sim_id)
    if not success:
        return jsonify({"error": "Simulation not found"}), 404
    return jsonify({"message": "Simulation deleted"}), 200
