from enum import Enum
from http import HTTPStatus
from werkzeug.security import generate_password_hash

from models import User
from utils import RegexPatterns
from extensions import db

import flask_login



class AuthResponses(Enum):
    """Classe responsável por fornecer as respostas da
    rota de autenticação.
    """

    CHECK_CREDENTIALS = {
        "authenticated": False,
        "status": "check_credentials",
        "redirect": None
    }

    BLOCKED = {
        "authenticated": False,
        "status": "blocked",
        "redirect": None
    }

    AUTHENTICATED = {
        "authenticated": True,
        "status": "authenticated",
        "redirect": "/system/"
    }

    INVALID_USERNAME = (
        {"msg": "Nome de usuário inválido!"}, HTTPStatus.UNAUTHORIZED
    )

    PASS_MISMATCH = (
        {"msg": "Senhas não conferem!"}, HTTPStatus.BAD_REQUEST
    )

    USER_CREATED = (
        {"msg": "Usuário criado com sucesso!"}, HTTPStatus.CREATED
    )

    USER_ALREADY_EXISTS = (
        {"msg": "Usuário já existente!"}, HTTPStatus.BAD_REQUEST
    )


class AuthService:
    """Classe responsável por lidar com a autenticação do usuário."""


    @classmethod
    def signup(cls, username: str, pass1: str, pass2, is_admin: bool):
        """Faz o hashing da senha fornecida retorna um HTTPStatus."""

        if not cls.is_valid_username(username):
            return AuthResponses.INVALID_USERNAME.value

        if User.find_by_username(username):
            return AuthResponses.USER_ALREADY_EXISTS.value

        if pass1 != pass2:
            return AuthResponses.PASS_MISMATCH.value

        password_hash = generate_password_hash(pass1)
        User.create(username, password_hash, is_admin)

        return AuthResponses.USER_CREATED.value


    @classmethod
    def signin(cls, username: str, password: str) -> dict:
        """Redireciona para a página principal caso o usuário e login sejam
        válidos."""

        user = User.find_by_username(username)

        if not user:
            return AuthResponses.CHECK_CREDENTIALS.value

        if not user.check_password(password):
            if not cls.handle_failed_attempt(user):
                return AuthResponses.BLOCKED.value

            return AuthResponses.CHECK_CREDENTIALS.value

        flask_login.logout_user()
        flask_login.login_user(user)
        user.misses = 0
        db.session.commit()

        return AuthResponses.AUTHENTICATED.value


    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Verifica se o USERNAME é válido."""

        pattern = RegexPatterns.USERNAME.value

        if not isinstance(username, str):
            return False

        if not username:
            return False

        if not pattern.fullmatch(username):
            return False

        return True


    @staticmethod
    def handle_failed_attempt(user: 'User') -> bool:
        """Incrementa tentativas falhas, verifica e bloqueia o usuário se
        necessário.

        Retorna True se o usuário está bloqueado, False caso contrário.
        """

        user.misses += 1

        if user.misses >= 3:
            user.is_active = False

        db.session.commit()
        return user.is_active
