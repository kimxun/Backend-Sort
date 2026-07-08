import random
import re
import smtplib
from email.message import EmailMessage
from flask import current_app
from redis.exceptions import RedisError
from werkzeug.security import check_password_hash, generate_password_hash
from app.database.db import db
from app.models.user import User
from app.config.cache import redis_client
from app.repositories.auth_repository import AuthRepository
from app.utils.jwt_helper import JwtHelper

class AuthService:
    OTP_TTL_SECONDS = 60
    OTP_KEY_PREFIX = "forgot_password"
    VERIFIED_KEY_PREFIX = "forgot_password_verified"

    @staticmethod
    def _normalize_email(email):
        return (email or "").strip().lower()

    @staticmethod
    def _validate_email(email):
        if not email:
            raise ValueError("Vui lòng nhập email")
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            raise ValueError("Email không đúng định dạng")

    @staticmethod
    def _validate_password(password):
        if not password:
            raise ValueError("Vui lòng nhập mật khẩu mới")
        if len(password) < 8:
            raise ValueError("Mật khẩu phải có ít nhất 8 ký tự")

    @staticmethod
    def _otp_key(email):
        return f"{AuthService.OTP_KEY_PREFIX}:{email}"

    @staticmethod
    def _verified_key(email):
        return f"{AuthService.VERIFIED_KEY_PREFIX}:{email}"

    @staticmethod
    def _send_reset_email(email, otp):
        smtp_host = current_app.config.get("SMTP_HOST")
        smtp_port = current_app.config.get("SMTP_PORT")
        smtp_user = current_app.config.get("SMTP_USER")
        smtp_password = current_app.config.get("SMTP_PASSWORD")
        smtp_from = current_app.config.get("SMTP_FROM")
        use_tls = current_app.config.get("SMTP_USE_TLS", True)

        if not smtp_host or not smtp_from:
            raise RuntimeError("Chưa cấu hình SMTP để gửi email")

        message = EmailMessage()
        message["Subject"] = "Xác nhận đặt lại mật khẩu"
        message["From"] = smtp_from
        message["To"] = email
        message.set_content(
            f"Mã OTP đặt lại mật khẩu của bạn là: {otp}\n\n"
            "OTP gồm 6 chữ số và chỉ có hiệu lực trong 60 giây.\n"
            "Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này."
        )

        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            if use_tls:
                server.starttls()
            if smtp_user and smtp_password:
                server.login(smtp_user, smtp_password)
            server.send_message(message)

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

    @staticmethod
    def forgot_password(email):
        email = AuthService._normalize_email(email)
        AuthService._validate_email(email)

        user = AuthRepository.find_by_email(email)
        if not user or user.status == 0:
            raise ValueError("Email không tồn tại trong hệ thống")

        otp = f"{random.SystemRandom().randint(0, 999999):06d}"
        otp_key = AuthService._otp_key(email)
        verified_key = AuthService._verified_key(email)

        try:
            redis_client.setex(otp_key, AuthService.OTP_TTL_SECONDS, otp)
            redis_client.delete(verified_key)
        except RedisError:
            raise RuntimeError("Không thể lưu OTP vào Redis")

        try:
            AuthService._send_reset_email(email, otp)
        except Exception as e:
            redis_client.delete(otp_key)
            print(e)
            raise RuntimeError(str(e))

        return {"message": "OTP đã được gửi đến email của bạn", "ttl": AuthService.OTP_TTL_SECONDS}

    @staticmethod
    def verify_otp(email, otp):
        email = AuthService._normalize_email(email)
        AuthService._validate_email(email)

        otp = (otp or "").strip()
        if not re.fullmatch(r"\d{6}", otp):
            raise ValueError("OTP phải gồm 6 chữ số")

        if not AuthRepository.find_by_email(email):
            raise ValueError("Email không khớp với yêu cầu OTP")

        otp_key = AuthService._otp_key(email)
        verified_key = AuthService._verified_key(email)

        try:
            saved_otp = redis_client.get(otp_key)
            ttl = redis_client.ttl(otp_key)
        except RedisError:
            raise RuntimeError("Không thể kiểm tra OTP trong Redis")

        if not saved_otp or ttl <= 0:
            raise ValueError("OTP đã hết hạn, vui lòng gửi lại")

        if saved_otp != otp:
            raise ValueError("OTP không chính xác")

        try:
            redis_client.setex(verified_key, ttl, "1")
        except RedisError:
            raise RuntimeError("Không thể xác nhận OTP trong Redis")

        return {"message": "Xác thực OTP thành công", "ttl": ttl}

    @staticmethod
    def reset_password(email, new_password, confirm_password):
        email = AuthService._normalize_email(email)
        AuthService._validate_email(email)

        if new_password != confirm_password:
            raise ValueError("Mật khẩu xác nhận không khớp")

        AuthService._validate_password(new_password)

        user = AuthRepository.find_by_email(email)
        if not user or user.status == 0:
            raise ValueError("Email không khớp với yêu cầu OTP")

        otp_key = AuthService._otp_key(email)
        verified_key = AuthService._verified_key(email)

        try:
            otp_exists = redis_client.exists(otp_key)
            verified = redis_client.get(verified_key)
        except RedisError:
            raise RuntimeError("Không thể kiểm tra trạng thái OTP trong Redis")

        if not otp_exists:
            raise ValueError("OTP đã hết hạn, vui lòng gửi lại")

        if verified != "1":
            raise ValueError("OTP chưa được xác thực hoặc email không khớp")

        AuthRepository.update_password(user, generate_password_hash(new_password))
        db.session.commit()

        try:
            redis_client.delete(otp_key, verified_key)
        except RedisError:
            pass

        return {"message": "Đổi mật khẩu thành công"}
