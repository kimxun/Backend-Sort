from flask import jsonify, Blueprint

from app.services.sort_service import SortService

algorithm_bp = Blueprint('algorithm', __name__)


@algorithm_bp.route('', methods=['GET'])
def get_all_algorithms():
    try:
        algorithms = SortService.get_all_algorithms()

        result = []

        for algorithm in algorithms:
            result.append(algorithm.to_dict())

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@algorithm_bp.route('/<int:algorithm_id>', methods=['GET'])
def get_algorithm(algorithm_id):
    try:
        algorithm = SortService.get_algorithm_by_id(algorithm_id)

        if not algorithm:
            return jsonify({"error": "Algorithm not found"}), 404

        return jsonify(algorithm.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
