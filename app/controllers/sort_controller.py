from flask import request, jsonify, Blueprint
import time
import json
from app.services.sort_service import sort_array_with_metrics, SortService

sort_bp = Blueprint('sort', __name__)

ALGO_SLUG_MAP = {
    'interchange_sort': 'interchange-sort',
    'quick_sort': 'quick-sort',
    'selection_sort': 'selection-sort'
}

def _get_algorithm_slug(algorithm_name):
    return ALGO_SLUG_MAP.get(algorithm_name)

def _measure_sorting(original_array, algorithm_name):
    start_time = time.time()
    sorted_array, steps, comparisons, swaps = sort_array_with_metrics(original_array, algorithm_name)
    end_time = time.time()
    execution_time_ms = int((end_time - start_time) * 1000)
    return sorted_array, steps, comparisons, swaps, execution_time_ms

def _build_response(original_array, sorted_array, algorithm_name, steps, comparisons, swaps, execution_time_ms, simulation_id=None, warning=None):
    response = {
        "original": original_array,
        "sorted": sorted_array,
        "algorithm": algorithm_name,
        "metrics": {
            "steps": steps,
            "comparisons": comparisons,
            "swaps": swaps,
            "execution_time_ms": execution_time_ms
        }
    }
    if simulation_id:
        response["simulation_id"] = simulation_id
    if warning:
        response["warning"] = warning
    return jsonify(response), 200

@sort_bp.route('', methods=['POST'])
def handle_sort():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    if 'array' not in data or 'algorithm' not in data:
        return jsonify({"error": "Missing 'array' or 'algorithm' field"}), 400
    if not isinstance(data['array'], list):
        return jsonify({"error": "'array' must be a list"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    original_array = data['array']
    algorithm_name = data['algorithm']
    user_id = data['user_id']

    if algorithm_name not in ALGO_SLUG_MAP:
        return jsonify({"error": f"Unsupported algorithm. Supported: {list(ALGO_SLUG_MAP.keys())}"}), 400

    try:
        sorted_array, steps, comparisons, swaps, exec_time = _measure_sorting(original_array, algorithm_name)
        slug = _get_algorithm_slug(algorithm_name)
        algorithm_obj = SortService.get_algorithm_by_slug(slug)

        if not algorithm_obj:
            return _build_response(original_array, sorted_array, algorithm_name,
                                   steps, comparisons, swaps, exec_time,
                                   warning="Algorithm not found in database, history not saved")

        history = SortService.save_simulation(
            user_id=user_id,
            algorithm_id=algorithm_obj.id,
            input_data=json.dumps(original_array),
            sorted_result=json.dumps(sorted_array),
            steps=steps,
            comparisons=comparisons,
            swaps=swaps,
            execution_time_ms=exec_time
        )
        return _build_response(original_array, sorted_array, algorithm_name,
                               steps, comparisons, swaps, exec_time,
                               simulation_id=history.id if history else None)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500