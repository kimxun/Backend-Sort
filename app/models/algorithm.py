from app.database.db import db


class Algorithm(db.Model):
    __tablename__ = 'ThuatToan'

    id = db.Column('idThuatToan', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('tenThuatToan', db.String(50), nullable=False)
    code = db.Column('codeThuatToan', db.Text)
    description = db.Column('moTa', db.String(255))
    time_complexity = db.Column('doPhucTapThoiGian', db.String(50))
    space_complexity = db.Column('doPhucBoNho', db.String(50))
    category_id = db.Column('loaiThuatToan', db.Integer, db.ForeignKey('LoaiThuatToan.idLoai'))
    slug = db.Column(db.String(50), unique=True, nullable=False)

    simulation_histories = db.relationship('SimulationHistory', backref='algorithm', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "time_complexity": self.time_complexity,
            "space_complexity": self.space_complexity,
            "category_id": self.category_id,
            "slug": self.slug
        }