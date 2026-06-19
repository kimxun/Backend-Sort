from app.database.db import db
from app.models.user import User

class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_query():
        return User.query

    @staticmethod
    def create(data):
        status = data.get('status', 1)
        user = User(
            username=data['username'],
            password=data['password'],
            full_name=data['full_name'],
            email=data['email'],
            role=data['role'],
            status=status
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user_id, data):
        user = User.query.get(user_id)
        if user:
            user.username = data.get('username', user.username)
            user.password = data.get('password', user.password)
            user.full_name = data.get('full_name', user.full_name)
            user.email = data.get('email', user.email)
            user.role = data.get('role', user.role)
            if 'status' in data:
                user.status = data['status']
            db.session.commit()
        return user

    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False