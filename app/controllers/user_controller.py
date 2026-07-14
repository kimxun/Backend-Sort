from flask import request, jsonify, Blueprint
from flasgger import swag_from
from werkzeug.security import generate_password_hash
from app.repositories.user_repository import UserRepository
from app.utils.auth_decorator import jwt_required, roles_required
from app.services.auth_service import AuthService
from app.services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('', methods=['GET'])
@jwt_required
@roles_required(1)
@swag_from('../apidocs/user_get_all.yml')
def get_all_users():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    result = UserService.get_all_users(page, limit)
    return jsonify(result), 200

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required
@swag_from('../apidocs/user_get_one.yml')
def get_user(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route('', methods=['POST'])
@jwt_required
@roles_required(1)
@swag_from('../apidocs/user_create.yml')
def create_user():
    data = request.get_json()
    print("🔥 RAW DATA:", data)
    print("🔥 TYPE:", type(data))
    required = ['username', 'password', 'full_name', 'email', 'role']
    if not all(k in data for k in required):
        return jsonify({"error": f"Missing fields, required: {required}"}), 400
    try:
      AuthService._validate_password(data['password'])
      data['password'] = generate_password_hash(data['password'])
      user = UserRepository.create(data)
      return jsonify(user.to_dict()), 201
    except Exception as e:
        print("🔥 ERROR FULL:", repr(e))   # 👈 THÊM DÒNG NÀY
        return jsonify({"error": str(e)}), 400

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required
@roles_required(1)
@swag_from('../apidocs/user_update.yml')
def update_user(user_id):
    data = request.get_json()
    try:
        if data.get('password'):
            AuthService._validate_password(data['password'])
            data['password'] = generate_password_hash(data['password'])
        else:
            data.pop('password', None)

        user = UserRepository.update(user_id, data)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required
@roles_required(1)
@swag_from('../apidocs/user_delete.yml')
def delete_user(user_id):
    data = request.get_json(silent=True) or {}
    permanent = data.get('permanent', False)
    success = UserRepository.delete(user_id, permanent=permanent)
    if not success:
        return jsonify({"error": "User not found or could not be deleted"}), 404
    return jsonify({"message": "User deleted"}), 200
