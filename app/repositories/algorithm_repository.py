from app.utils.db_connection import get_connection
from app.models.algorithm import Algorithm

class AlgorithmRepository:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idThuatToan as id, tenThuatToan as name, codeThuatToan as code,
                   moTa as description, doPhucTapThoiGian as time_complexity,
                   doPhucBoNho as space_complexity, loaiThuatToan as category_id, slug
            FROM ThuatToan
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Algorithm(**row) for row in rows]

    @staticmethod
    def get_by_id(algorithm_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idThuatToan as id, tenThuatToan as name, codeThuatToan as code,
                   moTa as description, doPhucTapThoiGian as time_complexity,
                   doPhucBoNho as space_complexity, loaiThuatToan as category_id, slug
            FROM ThuatToan WHERE idThuatToan = %s
        """, (algorithm_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Algorithm(**row) if row else None

    @staticmethod
    def get_by_slug(slug):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idThuatToan as id, tenThuatToan as name, codeThuatToan as code,
                   moTa as description, doPhucTapThoiGian as time_complexity,
                   doPhucBoNho as space_complexity, loaiThuatToan as category_id, slug
            FROM ThuatToan WHERE slug = %s
        """, (slug,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Algorithm(**row) if row else None

    @staticmethod
    def create(data):
        # data là dict: name, code, description, time_complexity, space_complexity, category_id, slug
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO ThuatToan 
            (tenThuatToan, codeThuatToan, moTa, doPhucTapThoiGian, doPhucBoNho, loaiThuatToan, slug)
            VALUES (%(name)s, %(code)s, %(description)s, %(time_complexity)s, %(space_complexity)s, %(category_id)s, %(slug)s)
        """
        cursor.execute(sql, data)
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return AlgorithmRepository.get_by_id(last_id)

    @staticmethod
    def update(algorithm_id, data):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE ThuatToan SET
                tenThuatToan = %(name)s,
                codeThuatToan = %(code)s,
                moTa = %(description)s,
                doPhucTapThoiGian = %(time_complexity)s,
                doPhucBoNho = %(space_complexity)s,
                loaiThuatToan = %(category_id)s,
                slug = %(slug)s
            WHERE idThuatToan = %(id)s
        """
        data['id'] = algorithm_id
        cursor.execute(sql, data)
        cursor.close()
        conn.close()
        return AlgorithmRepository.get_by_id(algorithm_id)

    @staticmethod
    def delete(algorithm_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ThuatToan WHERE idThuatToan = %s", (algorithm_id,))
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0