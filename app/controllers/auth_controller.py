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

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json() or {}

    try:
        result = AuthService.forgot_password(data.get("email"))
        return jsonify({
            "success": True,
            "data": result,
            "message": result["message"]
        }), 200
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

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json() or {}

    try:
        result = AuthService.verify_otp(data.get("email"), data.get("otp"))
        return jsonify({
            "success": True,
            "data": result,
            "message": result["message"]
        }), 200
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

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json() or {}

    try:
        result = AuthService.reset_password(
            data.get("email"),
            data.get("newPassword"),
            data.get("confirmPassword")
        )
        return jsonify({
            "success": True,
            "data": result,
            "message": result["message"]
        }), 200
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
