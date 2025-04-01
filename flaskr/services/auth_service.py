from typing import Optional
from models.user import User
from werkzeug.security import generate_password_hash
import flask_login
import re


class AuthService:
    """Classe responsável por lidar com a autenticação do usuário."""


    @staticmethod
    def create_user(username: str, password: str, 
                    is_admin=False):
        
        password_hash = generate_password_hash(password)
        user = User.create(username, password_hash, is_admin)

        return user
    

    @staticmethod
    def authenticate_user(username: str, password: str):
        user = User.find_by_username(username)
        
        if user:
            if user.check_password(password):
                flask_login.login_user(user)
                return True

        return False
    

    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Verifica se o USERNAME é válido."""

        if not isinstance(username, str):
            return False

        if not username:
            return False

        not_valid = re.search(r"[^\da-zA-Z\.\-\_]", username)
        
        if not_valid:
            return False
        
        return True
    

    @staticmethod
    def is_same_password(pass1: str, pass2: str) -> bool:
        """Verifica se ambas as senhas coincidem."""

        if pass1 != pass2:
            return False
    
        return True