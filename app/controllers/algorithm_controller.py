from flask import jsonify, Blueprint, request
from app.algorithms.selection_sort import selection_sort_logic
from app.algorithms.quick_sort import quick_sort_logic
from app.algorithms.interchange_sort import interchange_sort_logic
from app.services.sort_service import SortService

algorithm_bp = Blueprint('algorithm', __name__)

ALGO_FUNC_MAP = {
    'selection-sort': selection_sort_logic,
    'quick-sort': quick_sort_logic,
    'interchange-sort': interchange_sort_logic,
}

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
@algorithm_bp.route('/<int:algorithm_id>/steps', methods=['POST'])
def get_algorithm_steps(algorithm_id):
    data = request.get_json()
    if not data or 'array' not in data:
        return jsonify({"error": "Missing 'array' field"}), 400
    input_array = data['array']
    if not isinstance(input_array, list):
        return jsonify({"error": "'array' must be a list"}), 400

    algorithm = SortService.get_algorithm_by_id(algorithm_id)
    if not algorithm:
        return jsonify({"error": "Algorithm not found"}), 404

    func = ALGO_FUNC_MAP.get(algorithm.slug)
    if not func:
        return jsonify({"error": "Algorithm does not support step-by-step"}), 400

    try:
        sorted_arr, steps, comparisons, swaps, steps_history = func(input_array)
        return jsonify({
            "algorithm_id": algorithm_id,
            "algorithm_name": algorithm.name,
            "input_array": input_array,
            "sorted_array": sorted_arr,
            "steps": steps,
            "comparisons": comparisons,
            "swaps": swaps,
            "step_by_step": steps_history
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
