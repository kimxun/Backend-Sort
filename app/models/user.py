from app.database.db import db

class User(db.Model):
    __tablename__ = 'TaiKhoan'

    id = db.Column('idTaiKhoan', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('tenTaiKhoan', db.String(50), unique=True, nullable=False)
    password = db.Column('matKhau', db.String(255), nullable=False)
    full_name = db.Column('hoTen', db.String(50), nullable=False)
    email = db.Column('email', db.String(50), unique=True, nullable=False)
    role = db.Column('vaiTro', db.Integer, default=0)
    created_at = db.Column('ngayTao', db.DateTime, default=db.func.current_timestamp())
    status = db.Column('trangThai', db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.status
        }