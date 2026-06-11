from app.utils.db_connection import get_connection
from app.models.simulation_history import SimulationHistory

class SimulationHistoryRepository:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idLichSu as id, idTaiKhoan as user_id, idThuatToan as algorithm_id,
                   duLieuDauVao as input_data, ketQuaSapXep as sorted_result,
                   soBuoc as steps, soLanSoSanh as comparisons, soLanHoanDoi as swaps,
                   thoiGianXuLyMs as execution_time_ms, ngayThucHien as executed_at
            FROM LichSuMoPhong
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [SimulationHistory(**row) for row in rows]

    @staticmethod
    def get_by_id(history_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idLichSu as id, idTaiKhoan as user_id, idThuatToan as algorithm_id,
                   duLieuDauVao as input_data, ketQuaSapXep as sorted_result,
                   soBuoc as steps, soLanSoSanh as comparisons, soLanHoanDoi as swaps,
                   thoiGianXuLyMs as execution_time_ms, ngayThucHien as executed_at
            FROM LichSuMoPhong WHERE idLichSu = %s
        """, (history_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return SimulationHistory(**row) if row else None

    @staticmethod
    def get_by_user(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idLichSu as id, idTaiKhoan as user_id, idThuatToan as algorithm_id,
                   duLieuDauVao as input_data, ketQuaSapXep as sorted_result,
                   soBuoc as steps, soLanSoSanh as comparisons, soLanHoanDoi as swaps,
                   thoiGianXuLyMs as execution_time_ms, ngayThucHien as executed_at
            FROM LichSuMoPhong WHERE idTaiKhoan = %s
        """, (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [SimulationHistory(**row) for row in rows]

    @staticmethod
    def create(data):
        # data: user_id, algorithm_id, input_data, sorted_result,
        #       steps, comparisons, swaps, execution_time_ms
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO LichSuMoPhong 
            (idTaiKhoan, idThuatToan, duLieuDauVao, ketQuaSapXep, soBuoc, soLanSoSanh, soLanHoanDoi, thoiGianXuLyMs)
            VALUES (%(user_id)s, %(algorithm_id)s, %(input_data)s, %(sorted_result)s,
                    %(steps)s, %(comparisons)s, %(swaps)s, %(execution_time_ms)s)
        """
        cursor.execute(sql, data)
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return SimulationHistoryRepository.get_by_id(last_id)

    @staticmethod
    def update(history_id, data):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE LichSuMoPhong SET
                idTaiKhoan = %(user_id)s,
                idThuatToan = %(algorithm_id)s,
                duLieuDauVao = %(input_data)s,
                ketQuaSapXep = %(sorted_result)s,
                soBuoc = %(steps)s,
                soLanSoSanh = %(comparisons)s,
                soLanHoanDoi = %(swaps)s,
                thoiGianXuLyMs = %(execution_time_ms)s
            WHERE idLichSu = %(id)s
        """
        data['id'] = history_id
        cursor.execute(sql, data)
        cursor.close()
        conn.close()
        return SimulationHistoryRepository.get_by_id(history_id)

    @staticmethod
    def delete(history_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM LichSuMoPhong WHERE idLichSu = %s", (history_id,))
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0