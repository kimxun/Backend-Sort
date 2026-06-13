from app.database.db import db

class AlgorithmCategory(db.Model):
    __tablename__ = 'LoaiThuatToan'

    id = db.Column('idLoai', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('tenThuatToan', db.String(50))

    algorithms = db.relationship('Algorithm', backref='category', lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name}