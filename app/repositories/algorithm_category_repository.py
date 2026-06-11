from app.utils.db_connection import get_connection
from app.models.algorithm_category import AlgorithmCategory

class AlgorithmCategoryRepository:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT idLoai as id, tenThuatToan as name FROM LoaiThuatToan")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [AlgorithmCategory(**row) for row in rows]

    @staticmethod
    def get_by_id(category_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT idLoai as id, tenThuatToan as name FROM LoaiThuatToan WHERE idLoai = %s", (category_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return AlgorithmCategory(**row) if row else None

    @staticmethod
    def create(name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO LoaiThuatToan (tenThuatToan) VALUES (%s)", (name,))
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return AlgorithmCategoryRepository.get_by_id(last_id)

    @staticmethod
    def update(category_id, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE LoaiThuatToan SET tenThuatToan = %s WHERE idLoai = %s", (name, category_id))
        cursor.close()
        conn.close()
        return AlgorithmCategoryRepository.get_by_id(category_id)

    @staticmethod
    def delete(category_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM LoaiThuatToan WHERE idLoai = %s", (category_id,))
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0