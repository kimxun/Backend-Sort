import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

class JwtHelper:

    @staticmethod
    def generate_token(user):
        payload = {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        }

        return jwt.encode(
            payload,
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )