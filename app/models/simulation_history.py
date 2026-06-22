from app.database.db import db

class SimulationHistory(db.Model):
    __tablename__ = 'lichsumophong'

    id = db.Column('idLichSu', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('idTaiKhoan', db.Integer, db.ForeignKey('TaiKhoan.idTaiKhoan'))
    algorithm_id = db.Column('idThuatToan', db.Integer, db.ForeignKey('thuattoan.idThuatToan'))
    input_data = db.Column('duLieuDauVao', db.String(255))
    sorted_result = db.Column('ketQuaSapXep', db.String(255))
    steps = db.Column('soBuoc', db.Integer, default=0)
    comparisons = db.Column('soLanSoSanh', db.Integer, default=0)
    swaps = db.Column('soLanHoanDoi', db.Integer, default=0)
    execution_time_ms = db.Column('thoiGianXuLyMs', db.Integer, default=0)
    executed_at = db.Column('ngayThucHien', db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "algorithm_id": self.algorithm_id,
            "input_data": self.input_data,
            "sorted_result": self.sorted_result,
            "steps": self.steps,
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "execution_time_ms": self.execution_time_ms,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None
        }