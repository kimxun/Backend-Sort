from flask import request, jsonify, Blueprint
from flasgger import swag_from
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app.database.db import db
from app.repositories.auth_repository import AuthRepository
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
    data = request.get_json(silent=True) or {}
    required = ['username', 'password', 'full_name', 'email', 'role']
    field_labels = {
        'username': 'tên đăng nhập',
        'password': 'mật khẩu',
        'full_name': 'họ và tên',
        'email': 'email',
        'role': 'vai trò'
    }
    missing = [
        field for field in required
        if field not in data or (field != 'role' and not str(data.get(field, '')).strip())
    ]
    if missing:
        missing_labels = ', '.join(field_labels[field] for field in missing)
        return jsonify({"error": f"Vui lòng nhập: {missing_labels}"}), 400
    try:
        data['username'] = data['username'].strip()
        data['full_name'] = data['full_name'].strip()
        data['email'] = AuthService._normalize_email(data['email'])

        AuthService._validate_email(data['email'])
        AuthService._validate_password(data['password'])

        if UserRepository.get_by_username(data['username']):
            return jsonify({"error": "Tên tài khoản đã tồn tại"}), 400
        if AuthRepository.find_by_email(data['email']):
            return jsonify({"error": "Email đã tồn tại"}), 400

        data['password'] = generate_password_hash(data['password'])
        user = UserRepository.create(data)
        return jsonify(user.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Tên tài khoản hoặc email đã tồn tại"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required
@roles_required(1)
@swag_from('../apidocs/user_update.yml')
def update_user(user_id):
    data = request.get_json(silent=True) or {}
    try:
        current_user = UserRepository.get_by_id(user_id)
        if not current_user:
            return jsonify({"error": "User not found"}), 404

        if 'full_name' in data and isinstance(data['full_name'], str):
            data['full_name'] = data['full_name'].strip()
            if not data['full_name']:
                return jsonify({"error": "Vui lòng nhập họ và tên"}), 400

        if 'email' in data:
            if not str(data.get('email', '')).strip():
                return jsonify({"error": "Vui lòng nhập email"}), 400
            data['email'] = AuthService._normalize_email(data['email'])
            AuthService._validate_email(data['email'])
            existing_email_user = AuthRepository.find_by_email(data['email'])
            if existing_email_user and existing_email_user.id != user_id:
                return jsonify({"error": "Email đã tồn tại"}), 400

        if data.get('password'):
            AuthService._validate_password(data['password'])
            data['password'] = generate_password_hash(data['password'])
        else:
            data.pop('password', None)

        user = UserRepository.update(user_id, data)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict()), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Tên tài khoản hoặc email đã tồn tại"}), 400
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
