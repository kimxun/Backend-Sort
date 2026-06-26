from werkzeug.security import check_password_hash, generate_password_hash
from app.database.db import db
from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.utils.jwt_helper import JwtHelper

class AuthService:

    @staticmethod
    def login(username, password):

        user = AuthRepository.find_by_username(username)

        if not user:
            raise Exception("Tài khoản không tồn tại")

        if not check_password_hash(user.password, password):
            raise Exception("Sai mật khẩu")

        if user.status==0:
            raise Exception("Tài khoản đã xóa hoặc vô hiệu")
        token = JwtHelper.generate_token(user)

        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role
            }
        }

    @staticmethod
    def register(data):
        required = ["username", "password", "full_name", "email"]
        missing_fields = [field for field in required if not data.get(field)]

        if missing_fields:
            raise ValueError(f"Thiếu thông tin bắt buộc: {', '.join(missing_fields)}")

        username = data["username"].strip()
        email = data["email"].strip()

        if AuthRepository.find_by_username(username):
            raise ValueError("Tên tài khoản đã tồn tại")

        if AuthRepository.find_by_email(email):
            raise ValueError("Email đã tồn tại")

        user = User(
            username=username,
            password=generate_password_hash(data["password"]),
            full_name=data["full_name"].strip(),
            email=email,
            role=0
        )

        db.session.add(user)
        db.session.commit()

        token = JwtHelper.generate_token(user)

        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role
            }
        }
