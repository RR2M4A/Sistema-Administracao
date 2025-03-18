from models.user import User


class AuthService:
    """Classe responsável por lidar com a autenticação do usuário."""


    @staticmethod
    def authenticate_user(username: str, password: str):
        user = User.find_one(username)
        
        if user:
            if user.check_password(password):
                return user

        return None