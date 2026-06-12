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
