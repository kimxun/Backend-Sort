from werkzeug.security import check_password_hash
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