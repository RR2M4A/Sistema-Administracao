from models.user import User


class AuthService:
    
    @staticmethod
    def authenticate_user(username: str, password: str):
        user = User.find(username)
        
        if user:
            if user.check_password(password):
                return user

        return None