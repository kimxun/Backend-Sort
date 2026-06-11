from flask import request, jsonify, Blueprint
from repositories.user_repository import UserRepository

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('', methods=['GET'])
def get_all_users():
    users = UserRepository.get_all()
    return jsonify([u.to_dict() for u in users]), 200

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    required = ['username', 'password', 'full_name', 'email', 'role']
    if not all(k in data for k in required):
        return jsonify({"error": f"Missing fields, required: {required}"}), 400
    try:
        user = UserRepository.create(data)
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = UserRepository.update(user_id, data)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = UserRepository.delete(user_id)
    if not success:
        return jsonify({"error": "User not found or could not be deleted"}), 404
    return jsonify({"message": "User deleted"}), 200