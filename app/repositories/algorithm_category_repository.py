from app.database.db import db
from app.models.algorithm_category import AlgorithmCategory
from app.config.cache import cache


class AlgorithmCategoryRepository:
    @staticmethod
    @cache.memoize(timeout=300)
    def get_all():
        return AlgorithmCategory.query.filter(
            AlgorithmCategory.status != -1
        ).all()

    @staticmethod
    @cache.memoize(timeout=300)
    def get_by_id(category_id):
        return AlgorithmCategory.query.get(category_id)

    @staticmethod
    def create(name):
        category = AlgorithmCategory(
            name=name,
            status=1
        )

        db.session.add(category)
        db.session.commit()

        cache.delete_memoized(
            AlgorithmCategoryRepository.get_all
        )
        cache.delete_memoized(
            AlgorithmCategoryRepository.get_by_id,
            category.id
        )

        return category

    @staticmethod
    def update(category_id, name):
        category = AlgorithmCategory.query.get(category_id)

        if category:
            category.name = name

            db.session.commit()

            cache.delete_memoized(
                AlgorithmCategoryRepository.get_all
            )
            cache.delete_memoized(
                AlgorithmCategoryRepository.get_by_id,
                category.id
            )

        return category

    @staticmethod
    def delete(category_id, permanent=False):
        category = AlgorithmCategory.query.get(category_id)

        if not category:
            return False

        if permanent:
            db.session.delete(category)
        else:
            category.status = -1

        db.session.commit()

        cache.delete_memoized(
            AlgorithmCategoryRepository.get_all
        )
        cache.delete_memoized(
            AlgorithmCategoryRepository.get_by_id,
            category.id
        )

        return True

    @staticmethod
    def restore(category_id):
        category = AlgorithmCategory.query.get(category_id)

        if category and category.status == -1:
            category.status = 1

            db.session.commit()

            cache.delete_memoized(
                AlgorithmCategoryRepository.get_all
            )
            cache.delete_memoized(
                AlgorithmCategoryRepository.get_by_id,
                category.id
            )

            return True

        return False