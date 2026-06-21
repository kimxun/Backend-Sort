from app.models.user import User

class AuthRepository:
     @staticmethod
     def find_by_username(username):
        return User.query.filter_by(username=username).first()

     @staticmethod
     def find_by_email(email):
        return User.query.filter_by(email=email).first()
