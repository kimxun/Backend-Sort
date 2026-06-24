from flask import request, jsonify, Blueprint, g
import time
import json
from flasgger import swag_from
from app.services.sort_service import sort_array_with_metrics, SortService
from app.utils.auth_decorator import jwt_required,optional_jwt_required
from app.config.cache import cache
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
@optional_jwt_required
@swag_from('../apidocs/sort_post.yml')
def handle_sort():
    print("👉 DATA TỪ FRONTEND GỬI LÊN:", request.get_json())
    current_user = getattr(g, "current_user", None)
    
    # 1. KIỂM TRA LIMIT CỦA GUEST (Chỉ chạy khi không có token)
    if not current_user:
        guest_id = request.headers.get('Guest-ID')
        if not guest_id:
            return jsonify({"error": "Missing Guest-ID header"}), 400
        
        cache_key = f"free_sort:{guest_id}"
        count = cache.get(cache_key) or 0
        
        # Phải nằm trong khối if not current_user
        if count >= 3:
            return jsonify({
                "error": "Free limit exceeded", 
                "message": "Bạn đã sử dụng hết 3 lượt miễn phí. Vui lòng đăng nhập."
            }), 401
            
        # Tăng biến đếm và set timeout
        cache.set(cache_key, count + 1, timeout=86400)  # 24 giờ
        
    # 2. XỬ LÝ DỮ LIỆU ĐẦU VÀO
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    if 'array' not in data or 'algorithm' not in data:
        return jsonify({"error": "Missing 'array' or 'algorithm' field"}), 400
    if not isinstance(data['array'], list):
        return jsonify({"error": "'array' must be a list"}), 400

    original_array = data['array']
    algorithm_name = data['algorithm']
    algorithm_name = algorithm_name.lower().replace(' ', '_')
    
    # Lấy ID an toàn (Guest sẽ có user_id = None)
    user_id = current_user['id'] if current_user else None

    if algorithm_name not in ALGO_SLUG_MAP:
        return jsonify({"error": f"Unsupported algorithm. Supported: {list(ALGO_SLUG_MAP.keys())}"}), 400

    # 3. CHẠY THUẬT TOÁN VÀ LƯU DB
    try:
        sorted_array, steps, comparisons, swaps, exec_time = _measure_sorting(original_array, algorithm_name)
        slug = _get_algorithm_slug(algorithm_name)
        algorithm_obj = SortService.get_algorithm_by_slug(slug)

        simulation_id = None
        warning_msg = None

        if not algorithm_obj:
            warning_msg = "Algorithm not found in database, history not saved"
            
        elif current_user:  # <--- CHỈ LƯU VÀO DB NẾU LÀ USER ĐÃ ĐĂNG NHẬP
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
            simulation_id = history.id if history else None
        else:
            warning_msg = "Guest user: simulation history not saved."

        return _build_response(original_array, sorted_array, algorithm_name,
                               steps, comparisons, swaps, exec_time,
                               simulation_id=simulation_id, 
                               warning=warning_msg)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500