from app.database.db import db

class Algorithm(db.Model):
    __tablename__ = 'thuattoan'

    id = db.Column('idThuatToan', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('tenThuatToan', db.String(50), nullable=False)
    code = db.Column('codeThuatToan', db.Text)
    description = db.Column('moTa', db.String(255))
    time_complexity = db.Column('doPhucTapThoiGian', db.String(50))
    space_complexity = db.Column('doPhucBoNho', db.String(50))
    steps = db.Column('cacBuoc', db.Text)
    category_id = db.Column('loaiThuatToan', db.Integer, db.ForeignKey('loaithuattoan.idLoai'))
    slug = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column('trangThai', db.Integer, default=1)

    is_custom = db.Column(db.Boolean, default=False, nullable=False)
    code_filename = db.Column(db.String(255), nullable=True)

    simulation_histories = db.relationship('SimulationHistory', backref='algorithm', lazy=True)

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "time_complexity": self.time_complexity,
            "space_complexity": self.space_complexity,
            "steps": json.loads(self.steps) if self.steps else [],
            "category_id": self.category_id,
            "slug": self.slug,
            "status": self.status,
            "is_custom": self.is_custom,
            "code_filename": self.code_filename
        }