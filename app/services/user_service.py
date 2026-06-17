from app.repositories.user_repository import UserRepository

class UserService:

    @staticmethod
    def get_all_users(page, limit):
        if page < 1:
            page = 1
        if limit < 1:
            limit = 10

        query = UserRepository.get_query()

        total = query.count()

        users = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "data": [u.to_dict() for u in users],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": (total + limit - 1) // limit
            }
        }