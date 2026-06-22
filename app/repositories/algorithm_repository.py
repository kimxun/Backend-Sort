from app.database.db import db
from app.models.algorithm import Algorithm
from app.config.cache import cache

class AlgorithmRepository:
    @staticmethod
    @cache.memoize(timeout=300)
    def get_all(is_admin=False):
        if is_admin:
            return Algorithm.query.filter(Algorithm.status != -1).all()
        return Algorithm.query.filter_by(status=1).all()

    @staticmethod
    @cache.memoize(timeout=300)
    def get_by_id(algorithm_id):
        return Algorithm.query.get(algorithm_id)

    @staticmethod
    @cache.memoize(timeout=300)
    def get_by_slug(slug):
        return Algorithm.query.filter_by(slug=slug).first()

    @staticmethod
    def get_query():
        return Algorithm.query

    @staticmethod
    def create(data):
        algorithm = Algorithm(
            name=data['name'],
            code=data.get('code', ''),
            description=data.get('description', ''),
            time_complexity=data.get('time_complexity', ''),
            space_complexity=data.get('space_complexity', ''),
            steps=data.get('steps'),
            category_id=data.get('category_id', 1),
            slug=data['slug'],
            status=data.get('status', 1)
        )
        db.session.add(algorithm)
        db.session.commit()
        cache.delete_memoized(AlgorithmRepository.get_all)
        cache.delete_memoized(AlgorithmRepository.get_by_id, algorithm.id)
        cache.delete_memoized(AlgorithmRepository.get_by_slug, algorithm.slug)
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
            algorithm.steps = data.get('steps', algorithm.steps)
            algorithm.category_id = data.get('category_id', algorithm.category_id)
            algorithm.slug = data.get('slug', algorithm.slug)
            if 'status' in data:
                algorithm.status = data['status']
            db.session.commit()
            cache.delete_memoized(AlgorithmRepository.get_all)
            cache.delete_memoized(AlgorithmRepository.get_by_id, algorithm.id)
            cache.delete_memoized(AlgorithmRepository.get_by_slug, algorithm.slug)
        return algorithm

    @staticmethod
    def delete(algorithm_id):
        algorithm = Algorithm.query.get(algorithm_id)
        if algorithm:
            algorithm.status = -1
            db.session.commit()
            cache.delete_memoized(AlgorithmRepository.get_all)
            cache.delete_memoized(AlgorithmRepository.get_by_id, algorithm.id)
            cache.delete_memoized(AlgorithmRepository.get_by_slug, algorithm.slug)
            return True
        return False