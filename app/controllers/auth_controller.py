from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
@swag_from('../apidocs/auth_login.yml')
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        result = AuthService.login(username, password)
        return jsonify({
            "success": True,
            "data": result
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 401

@auth_bp.route("/register", methods=["POST"])
@swag_from('../apidocs/auth_register.yml')
def register():
    data = request.get_json() or {}

    try:
        result = AuthService.register(data)
        return jsonify({
            "success": True,
            "data": result
        }), 201
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
