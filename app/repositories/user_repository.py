from app.utils.db_connection import get_connection
from app.models.user import User

class UserRepository:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idTaiKhoan as id, tenTaiKhoan as username, matKhau as password,
                   hoTen as full_name, email, vaiTro as role, ngayTao as created_at
            FROM TaiKhoan
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [User(**row) for row in rows]

    @staticmethod
    def get_by_id(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idTaiKhoan as id, tenTaiKhoan as username, matKhau as password,
                   hoTen as full_name, email, vaiTro as role, ngayTao as created_at
            FROM TaiKhoan WHERE idTaiKhoan = %s
        """, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return User(**row) if row else None

    @staticmethod
    def get_by_username(username):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idTaiKhoan as id, tenTaiKhoan as username, matKhau as password,
                   hoTen as full_name, email, vaiTro as role, ngayTao as created_at
            FROM TaiKhoan WHERE tenTaiKhoan = %s
        """, (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return User(**row) if row else None

    @staticmethod
    def create(data):
        # data: username, password, full_name, email, role
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO TaiKhoan (tenTaiKhoan, matKhau, hoTen, email, vaiTro)
            VALUES (%(username)s, %(password)s, %(full_name)s, %(email)s, %(role)s)
        """
        cursor.execute(sql, data)
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return UserRepository.get_by_id(last_id)

    @staticmethod
    def update(user_id, data):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE TaiKhoan SET
                tenTaiKhoan = %(username)s,
                matKhau = %(password)s,
                hoTen = %(full_name)s,
                email = %(email)s,
                vaiTro = %(role)s
            WHERE idTaiKhoan = %(id)s
        """
        data['id'] = user_id
        cursor.execute(sql, data)
        cursor.close()
        conn.close()
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def delete(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM TaiKhoan WHERE idTaiKhoan = %s", (user_id,))
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0