from flask import request, jsonify, Blueprint
from app.services.sort_service import sort_array

sort_bp = Blueprint('sort', __name__)


@sort_bp.route('', methods=['POST'])
def handle_sort():

    data = request.get_json()
    if not data or 'array' not in data or 'algorithm' not in data:
        return jsonify({"error": "Missing 'array' or 'algorithm' field"}), 400

    original_array = data['array']
    algorithm = data['algorithm']

    try:
        sorted_array = sort_array(original_array, algorithm)
        return jsonify({
            "original": original_array,
            "sorted": sorted_array,
            "algorithm": algorithm
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400