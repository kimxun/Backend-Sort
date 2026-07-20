import os
from flask import jsonify, Blueprint, request, current_app, g
from flasgger import swag_from
import traceback
import json
import jwt
import time
import hashlib
from app.algorithms.selection_sort import selection_sort_logic
from app.algorithms.quick_sort import quick_sort_logic
from app.algorithms.interchange_sort import interchange_sort_logic
from app.algorithms.search.linear_search import linear_search_logic
from app.algorithms.search.binary_search import binary_search_logic
from app.services.sort_service import SortService
from app.repositories.algorithm_repository import AlgorithmRepository
from app.utils.auth_decorator import jwt_required, roles_required
from app.services.algorithm_validator import (
    validate_and_save_algorithm_file,
    load_uploaded_algorithm_function,
    AlgorithmValidationError,
)
from app.config.cache import cache

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

MAX_UPLOAD_SIZE = 200 * 1024
FREE_TIER_LIMIT = 3
FREE_TIER_RESET_SECONDS = 86400


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


def _get_user_or_guest():
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            return payload, None
        except Exception:
            pass
    user_ip = request.remote_addr or "unknown_ip"
    user_agent = request.headers.get("User-Agent", "unknown_device")
    raw_identifier = f"{user_ip}_{user_agent}"
    guest_id = hashlib.md5(raw_identifier.encode("utf-8")).hexdigest()
    return None, guest_id


def _check_free_tier_and_increment(guest_id):
    if not guest_id:
        return True
    cache_key = f"free_tier:{guest_id}"
    count = cache.get(cache_key)
    if count is None:
        cache.set(cache_key, 1, timeout=FREE_TIER_RESET_SECONDS)
        return True
    try:
        count = int(count)
    except (TypeError, ValueError):
        cache.set(cache_key, 1, timeout=FREE_TIER_RESET_SECONDS)
        return True
    if count >= FREE_TIER_LIMIT:
        return False
    cache.set(cache_key, count + 1, timeout=FREE_TIER_RESET_SECONDS)
    return True


def _is_blank_field(value):
    if value is None:
        return True
    if isinstance(value, list):
        return len(value) == 0
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return True
        if stripped.startswith('['):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return len(parsed) == 0
            except (ValueError, TypeError):
                return False
        return False
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
        required = ['name', 'slug', 'description', 'steps']
        missing = [k for k in required if _is_blank_field(data.get(k))]
        if missing:
            return jsonify({
                "error": f"Vui lòng nhập đầy đủ thông tin bắt buộc: {', '.join(missing)}"
            }), 400

        if data.get('is_custom') and data['slug'] in ALGO_FUNC_MAP:
            return jsonify({
                "error": (
                    f"Slug '{data['slug']}' trùng với thuật toán hệ thống đã có sẵn. "
                    "File upload của bạn sẽ KHÔNG được dùng vì hệ thống ưu tiên thuật toán "
                    "hardcode trước. Vui lòng đổi tên file/slug khác."
                )
            }), 400

        data.setdefault('category_id', 1)
        data.setdefault('status', 1)
        data.setdefault('code', '')
        data.setdefault('time_complexity', '')
        data.setdefault('space_complexity', '')
        data.setdefault('is_custom', False)
        data.setdefault('code_filename', None)
        data.setdefault('features', None)
        if data.get('code_filename'):
            data['is_custom'] = True
        if data['is_custom'] and not data.get('code_filename'):
            return jsonify({
                "error": "Thiếu code_filename. Vui lòng upload file thuật toán trước khi lưu."
            }), 400

        if 'steps' in data and data['steps'] is not None:
            if isinstance(data['steps'], list):
                data['steps'] = json.dumps(data['steps'])
            elif isinstance(data['steps'], str) and data['steps'].strip() == '':
                data['steps'] = None

        if 'features' in data and isinstance(data['features'], list):
            data['features'] = json.dumps(data['features'])

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
def sort_algorithm():
    data = request.get_json()
    if not data or 'array' not in data:
        return jsonify({"error": "Missing 'array' field"}), 400
    input_array = data['array']
    if not isinstance(input_array, list):
        return jsonify({"error": "'array' must be a list"}), 400

    user, guest_id = _get_user_or_guest()

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
    if not func and algorithm.code_filename:
        func = load_uploaded_algorithm_function(algorithm.code_filename.replace('.py', ''))
    if not func:
        return jsonify({"error": "Algorithm does not support step-by-step"}), 400

    try:
        start_time = time.perf_counter()
        sorted_arr, steps_count, comparisons, swaps, steps_history = func(input_array, sort_order)
        execution_time_ms = int((time.perf_counter() - start_time) * 1000)

        if user:
            SortService.save_simulation(
                user_id=user["id"],
                algorithm_id=algorithm.id,
                input_data=json.dumps(input_array),
                sorted_result=json.dumps(sorted_arr),
                steps=steps_count,
                comparisons=comparisons,
                swaps=swaps,
                execution_time_ms=execution_time_ms
            )

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
@swag_from('../apidocs/algorithms_post_steps.yml')
def get_algorithm_steps(algorithm_id):
    data = request.get_json()
    if not data or 'array' not in data:
        return jsonify({"error": "Missing 'array' field"}), 400
    input_array = data['array']
    if not isinstance(input_array, list):
        return jsonify({"error": "'array' must be a list"}), 400

    user, guest_id = _get_user_or_guest()
    if not user and not guest_id:
        return jsonify({"error": "Guest ID required"}), 400

    sort_order = data.get('sortOrder', 'asc')

    algorithm = SortService.get_algorithm_by_id(algorithm_id)
    if not algorithm:
        return jsonify({"error": "Algorithm not found"}), 404

    func = ALGO_FUNC_MAP.get(algorithm.slug)
    if not func and algorithm.code_filename:
        func = load_uploaded_algorithm_function(algorithm.code_filename.replace('.py', ''))
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
def search_algorithm_steps(algorithm_id):
    data = request.get_json()
    if not data or 'array' not in data or 'target' not in data:
        return jsonify({"error": "Missing 'array' or 'target'"}), 400
    input_array = data['array']
    target = data['target']
    if not isinstance(input_array, list):
        return jsonify({"error": "'array' must be a list"}), 400

    user, guest_id = _get_user_or_guest()
    if not user and not guest_id:
        return jsonify({"error": "Guest ID required"}), 400

    algorithm = SortService.get_algorithm_by_id(algorithm_id)
    if not algorithm:
        return jsonify({"error": "Algorithm not found"}), 404

    func = SEARCH_FUNC_MAP.get(algorithm.slug)
    if not func:
        return jsonify({"error": "Search algorithm not implemented"}), 400

    try:
        start_time = time.perf_counter()

        if algorithm.slug == 'binary-search':
            input_array = sorted(input_array)

        steps, comparisons, found_index = func(input_array, target)
        execution_time_ms = int((time.perf_counter() - start_time) * 1000)

        if user:
            SortService.save_simulation(
                user_id=user["id"],
                algorithm_id=algorithm.id,
                input_data=json.dumps(input_array),
                sorted_result=json.dumps({
                    "target": target,
                    "found_index": found_index
                }),
                steps=steps,
                comparisons=comparisons,
                swaps=0,
                execution_time_ms=execution_time_ms
            )

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


@algorithm_bp.route('/compare', methods=['POST'])
@jwt_required
def compare_algorithms():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    if not data or 'array' not in data or 'algorithm_id_1' not in data or 'algorithm_id_2' not in data:
        return jsonify({"error": "Thiếu trường bắt buộc: array, algorithm_id_1, algorithm_id_2"}), 400

    input_array = data['array']
    if not isinstance(input_array, list):
        return jsonify({"error": "'array' must be a list"}), 400

    id1 = data['algorithm_id_1']
    id2 = data['algorithm_id_2']
    sort_order = data.get('sortOrder', 'asc')

    algo1 = SortService.get_algorithm_by_id(id1)
    algo2 = SortService.get_algorithm_by_id(id2)
    if not algo1 or not algo2:
        return jsonify({"error": "Không tìm thấy thuật toán"}), 404

    func1 = ALGO_FUNC_MAP.get(algo1.slug)
    if not func1 and algo1.code_filename:
        func1 = load_uploaded_algorithm_function(algo1.code_filename.replace('.py', ''))
    func2 = ALGO_FUNC_MAP.get(algo2.slug)
    if not func2 and algo2.code_filename:
        func2 = load_uploaded_algorithm_function(algo2.code_filename.replace('.py', ''))

    if not func1 or not func2:
        return jsonify({"error": "Một trong hai thuật toán không hỗ trợ chạy từng bước"}), 400

    try:
        start1 = time.perf_counter()
        sorted1, steps1, comps1, swaps1, _ = func1(input_array.copy(), sort_order)
        time1 = int((time.perf_counter() - start1) * 1000)

        start2 = time.perf_counter()
        sorted2, steps2, comps2, swaps2, _ = func2(input_array.copy(), sort_order)
        time2 = int((time.perf_counter() - start2) * 1000)

        return jsonify({
            "algorithm_1": {
                "id": algo1.id,
                "name": algo1.name,
                "slug": algo1.slug,
                "steps": steps1,
                "comparisons": comps1,
                "swaps": swaps1,
                "time_ms": time1,
                "sorted": sorted1
            },
            "algorithm_2": {
                "id": algo2.id,
                "name": algo2.name,
                "slug": algo2.slug,
                "steps": steps2,
                "comparisons": comps2,
                "swaps": swaps2,
                "time_ms": time2,
                "sorted": sorted2
            },
            "input_array": input_array,
            "sort_order": sort_order
        }), 200
    except Exception as e:
        print("LỖI POST /compare:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@algorithm_bp.route('/<int:algorithm_id>', methods=['PUT'])
@jwt_required
@roles_required(1)
def update_algorithm(algorithm_id):
    try:
        if request.method == 'OPTIONS':
            return '', 200

        data = request.get_json()

        if data.get('is_custom') and data.get('slug') in ALGO_FUNC_MAP:
            return jsonify({
                "error": (
                    f"Slug '{data['slug']}' trùng với thuật toán hệ thống đã có sẵn. "
                    "Vui lòng đổi slug khác cho thuật toán tuỳ chỉnh."
                )
            }), 400

        if 'steps' in data and data['steps'] is not None:
            if isinstance(data['steps'], list):
                data['steps'] = json.dumps(data['steps'])
            elif isinstance(data['steps'], str) and data['steps'].strip() == '':
                data['steps'] = None

        if 'features' in data and isinstance(data['features'], list):
            data['features'] = json.dumps(data['features'])

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


@algorithm_bp.route('/upload-code', methods=['POST'])
@jwt_required
@roles_required(1)
def upload_algorithm_code():
    if request.method == 'OPTIONS':
        return '', 200

    if 'file' not in request.files:
        return jsonify({"error": "Không tìm thấy file"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Tên file rỗng"}), 400

    try:
        slug, filepath, display_code, features, time_comp, space_comp = validate_and_save_algorithm_file(file, file.filename)
        return jsonify({
            "slug": slug,
            "code_filename": os.path.basename(filepath),
            "display_code": display_code or "",
            "features": features,
            "time_complexity": time_comp or "",
            "space_complexity": space_comp or ""
        }), 200
    except AlgorithmValidationError as e:
        return jsonify({"error": str(e)}), 400