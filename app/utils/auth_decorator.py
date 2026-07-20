import jwt
from functools import wraps
from flask import request, jsonify, current_app, g

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            return f(*args, **kwargs)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "message": "Thiếu token"
            }), 401

        try:
            parts = auth_header.split()

            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify({
                    "message": "Authorization header không hợp lệ"
                }), 401

            token = parts[1]

            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            g.current_user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({
                "message": "Token đã hết hạn"
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "message": "Token không hợp lệ"
            }), 401

        return f(*args, **kwargs)

    return decorated


def roles_required(*roles):
    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):
            if request.method == 'OPTIONS':
                return f(*args, **kwargs)

            current_user = getattr(g, "current_user", None)
            print("Current User in roles_required:", current_user)
            if not current_user:
                return jsonify({
                    "message": "Chưa xác thực"
                }), 401

            user_role = current_user.get("role")
            print("User Role:", user_role)
            if user_role not in roles:
                return jsonify({
                    "message": "Bạn không có quyền truy cập"
                }), 403

            return f(*args, **kwargs)

        return decorated

    return decorator


def optional_jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        g.current_user = None

        if auth_header:
            try:
                parts = auth_header.split()

                if len(parts) == 2 and parts[0] == "Bearer":
                    token = parts[1]

                    payload = jwt.decode(
                        token,
                        current_app.config["SECRET_KEY"],
                        algorithms=["HS256"]
                    )

                    g.current_user = payload

            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                pass

        return f(*args, **kwargs)

    return decorated