from flask import request, jsonify, Blueprint, g
import time
import json
import hashlib # THÊM THƯ VIỆN NÀY ĐỂ BĂM MÃ hóa MD5
from flasgger import swag_from
from app.services.sort_service import sort_array_with_metrics, SortService
from app.utils.auth_decorator import jwt_required, optional_jwt_required
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
    current_user = getattr(g, "current_user", None)
    
    if not current_user:
        user_ip = request.remote_addr # Lấy IP người dùng gửi lên
        user_agent = request.headers.get('User-Agent', '') # Lấy thông tin chi tiết về trình duyệt/thiết bị
        
        # Tạo chuỗi định danh kết hợp:
        raw_identifier = f"{user_ip}_{user_agent}"
        
        # Băm chuỗi trên thành 1 mã MD5 duy nhất
        device_id = hashlib.md5(raw_identifier.encode()).hexdigest()
        
        # Sử dụng device_id tự động này làm key định danh trong Redis cache
        cache_key = f"free_sort:{device_id}"
        count = cache.get(cache_key) or 0
        
        if count >= 3:
            return jsonify({
                "error": "Free limit exceeded", 
                "message": "Bạn đã sử dụng hết 3 lượt miễn phí. Vui lòng đăng nhập. Hoặc đợi 24h để sử dụng tiếp."
            }), 401
            
        # Tăng biến đếm và set timeout
        cache.set(cache_key, count + 1, timeout=86400)  # 24 giờ
        

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
    
    user_id = current_user['id'] if current_user else None

    if algorithm_name not in ALGO_SLUG_MAP:
        return jsonify({"error": f"Unsupported algorithm. Supported: {list(ALGO_SLUG_MAP.keys())}"}), 400

   
    try:
        sorted_array, steps, comparisons, swaps, exec_time = _measure_sorting(original_array, algorithm_name)
        slug = _get_algorithm_slug(algorithm_name)
        algorithm_obj = SortService.get_algorithm_by_slug(slug)

        simulation_id = None
        warning_msg = None

        if not algorithm_obj:
            warning_msg = "Algorithm not found in database, history not saved"
            
        elif current_user:  
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