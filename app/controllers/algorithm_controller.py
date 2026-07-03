from flask import jsonify, Blueprint, request, current_app
from flasgger import swag_from
import traceback
import json
import jwt
from app.algorithms.selection_sort import selection_sort_logic
from app.algorithms.quick_sort import quick_sort_logic
from app.algorithms.interchange_sort import interchange_sort_logic
from app.algorithms.search.linear_search import linear_search_logic
from app.algorithms.search.binary_search import binary_search_logic
from app.services.sort_service import SortService
from app.repositories.algorithm_repository import AlgorithmRepository
from app.utils.auth_decorator import jwt_required, roles_required

algorithm_bp = Blueprint('algorithm', __name__)

ALGO_FUNC_MAP = {
    'selection-sort': selection_sort_logic,
    'quick-sort': quick_sort_logic,
    'interchange-sort': interchange_sort_logic,
}

SEARCH_FUNC_MAP = {
    'linear-search': linear_search_logic,
    'binary-search': binary_search_logic,
}


def _is_admin_request():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return False
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload.get('role') == 1
    except:
        return False


@algorithm_bp.route('', methods=['GET'])
@swag_from('../apidocs/algorithms_get_all.yml')
def get_all_algorithms():
    try:
        is_admin = _is_admin_request()
        page = request.args.get('page', None, type=int)
        if page is not None:
            limit = request.args.get('limit', 5, type=int)
            result = SortService.get_all_algorithms(page, limit, is_admin=is_admin)
            return jsonify(result), 200
        else:
            algorithms = SortService.get_all_algorithms(is_admin=is_admin)
            return jsonify([a.to_dict() for a in algorithms]), 200
    except Exception as e:
        print("LỖI GET /algorithms:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@algorithm_bp.route('', methods=['POST'])
@jwt_required
@roles_required(1)
def create_algorithm():
    try:
        data = request.get_json()
        required = ['name', 'slug']
        if not all(k in data for k in required):
            return jsonify({"error": f"Missing required fields: {required}"}), 400

        data.setdefault('category_id', 1)
        data.setdefault('status', 1)
        data.setdefault('code', '')
        data.setdefault('description', '')
        data.setdefault('time_complexity', '')
        data.setdefault('space_complexity', '')
        data.setdefault('steps', None)

        if 'steps' in data and data['steps'] is not None:
            if isinstance(data['steps'], list):
                data['steps'] = json.dumps(data['steps'])
            elif isinstance(data['steps'], str) and data['steps'].strip() == '':
                data['steps'] = None

        new_algorithm = SortService.create_algorithm(data)
        return jsonify(new_algorithm.to_dict()), 201
    except Exception as e:
        print("LỖI POST /algorithms:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@algorithm_bp.route('/<int:algorithm_id>', methods=['GET'])
@swag_from('../apidocs/algorithms_get_one.yml')
def get_algorithm(algorithm_id):
    try:
        algorithm = SortService.get_algorithm_by_id(algorithm_id)
        if not algorithm:
            return jsonify({"error": "Algorithm not found"}), 404
        return jsonify(algorithm.to_dict()), 200
    except Exception as e:
        print("LỖI GET /algorithms/<id>:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@algorithm_bp.route('/sort', methods=['POST'])
@jwt_required
def sort_algorithm():
    data = request.get_json()
    if not data or 'array' not in data:
        return jsonify({"error": "Missing 'array' field"}), 400
    input_array = data['array']
    if not isinstance(input_array, list):
        return jsonify({"error": "'array' must be a list"}), 400

    algorithm_id = data.get('algorithm_id')
    algorithm_slug = data.get('algorithm')
    sort_order = data.get('sortOrder', 'asc')

    algorithm = None
    if algorithm_id:
        algorithm = SortService.get_algorithm_by_id(algorithm_id)
    if not algorithm and algorithm_slug:
        algorithm = AlgorithmRepository.get_by_slug(algorithm_slug)
    if not algorithm:
        return jsonify({"error": "Algorithm not found"}), 404

    func = ALGO_FUNC_MAP.get(algorithm.slug)
    if not func:
        return jsonify({"error": "Algorithm does not support step-by-step"}), 400

    try:
        sorted_arr, steps_count, comparisons, swaps, steps_history = func(input_array, sort_order)
        return jsonify({
            "algorithm": algorithm.slug,
            "algorithm_id": algorithm.id,
            "algorithm_name": algorithm.name,
            "original": input_array,
            "sorted": sorted_arr,
            "steps": steps_count,
            "step_by_step": steps_history,
            "comparisons": comparisons,
            "swaps": swaps
        }), 200
    except Exception as e:
        print("LỖI POST /sort:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@algorithm_bp.route('/<int:algorithm_id>/steps', methods=['POST'])
@jwt_required
@swag_from('../apidocs/algorithms_post_steps.yml')
def get_algorithm_steps(algorithm_id):
    data = request.get_json()
    if not data or 'array' not in data:
        return jsonify({"error": "Missing 'array' field"}), 400
    input_array = data['array']
    if not isinstance(input_array, list):
        return jsonify({"error": "'array' must be a list"}), 400

    sort_order = data.get('sortOrder', 'asc')

    algorithm = SortService.get_algorithm_by_id(algorithm_id)
    if not algorithm:
        return jsonify({"error": "Algorithm not found"}), 404

    func = ALGO_FUNC_MAP.get(algorithm.slug)
    if not func:
        return jsonify({"error": "Algorithm does not support step-by-step"}), 400

    try:
        sorted_arr, steps, comparisons, swaps, steps_history = func(input_array, sort_order)
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
        print("LỖI POST /steps:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@algorithm_bp.route('/<int:algorithm_id>/search', methods=['POST'])
@jwt_required
def search_algorithm_steps(algorithm_id):
    data = request.get_json()
    if not data or 'array' not in data or 'target' not in data:
        return jsonify({"error": "Missing 'array' or 'target'"}), 400
    input_array = data['array']
    target = data['target']
    if not isinstance(input_array, list):
        return jsonify({"error": "'array' must be a list"}), 400

    algorithm = SortService.get_algorithm_by_id(algorithm_id)
    if not algorithm:
        return jsonify({"error": "Algorithm not found"}), 404

    func = SEARCH_FUNC_MAP.get(algorithm.slug)
    if not func:
        return jsonify({"error": "Search algorithm not implemented"}), 400

    try:
        if algorithm.slug == 'binary-search':
            input_array = sorted(input_array)

        steps, comparisons, found_index = func(input_array, target)
        return jsonify({
            'algorithm_id': algorithm_id,
            'algorithm_name': algorithm.name,
            'input_array': input_array,
            'target': target,
            'steps': steps,
            'comparisons': comparisons,
            'found_index': found_index
        }), 200
    except Exception as e:
        print("LỖI POST /search:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@algorithm_bp.route('/<int:algorithm_id>', methods=['PUT'])
@jwt_required
@roles_required(1)
def update_algorithm(algorithm_id):
    try:
        data = request.get_json()
        if 'steps' in data and data['steps'] is not None:
            if isinstance(data['steps'], list):
                data['steps'] = json.dumps(data['steps'])
            elif isinstance(data['steps'], str) and data['steps'].strip() == '':
                data['steps'] = None

        updated = SortService.update_algorithm(algorithm_id, data)
        if not updated:
            return jsonify({"error": "Algorithm not found"}), 404
        return jsonify(updated.to_dict()), 200
    except Exception as e:
        print("LỖI PUT /algorithms/<id>:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@algorithm_bp.route('/<int:algorithm_id>', methods=['DELETE'])
@jwt_required
@roles_required(1)
def delete_algorithm(algorithm_id):
    try:
        data = request.get_json(silent=True) or {}
        permanent = data.get('permanent', False)
        success = SortService.delete_algorithm(algorithm_id, permanent=permanent)
        if not success:
            return jsonify({"error": "Algorithm not found"}), 404
        return jsonify({"message": "Algorithm deleted"}), 200
    except Exception as e:
        print("LỖI DELETE /algorithms/<id>:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500