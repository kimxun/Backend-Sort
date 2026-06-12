from app.database.db import db
from app.models.algorithm import Algorithm

class AlgorithmRepository:
    @staticmethod
    def get_all():
        return Algorithm.query.all()

    @staticmethod
    def get_by_id(algorithm_id):
        return Algorithm.query.get(algorithm_id)

    @staticmethod
    def get_by_slug(slug):
        return Algorithm.query.filter_by(slug=slug).first()

    @staticmethod
    def create(data):
        algorithm = Algorithm(
            name=data['name'],
            code=data['code'],
            description=data['description'],
            time_complexity=data['time_complexity'],
            space_complexity=data['space_complexity'],
            category_id=data['category_id'],
            slug=data['slug']
        )
        db.session.add(algorithm)
        db.session.commit()
        return algorithm

    @staticmethod
    def update(algorithm_id, data):
        algorithm = Algorithm.query.get(algorithm_id)
        if algorithm:
            algorithm.name = data.get('name', algorithm.name)
            algorithm.code = data.get('code', algorithm.code)
            algorithm.description = data.get('description', algorithm.description)
            algorithm.time_complexity = data.get('time_complexity', algorithm.time_complexity)
            algorithm.space_complexity = data.get('space_complexity', algorithm.space_complexity)
            algorithm.category_id = data.get('category_id', algorithm.category_id)
            algorithm.slug = data.get('slug', algorithm.slug)
            db.session.commit()
        return algorithm

    @staticmethod
    def delete(algorithm_id):
        algorithm = Algorithm.query.get(algorithm_id)
        if algorithm:
            db.session.delete(algorithm)
            db.session.commit()
            return True
        return False