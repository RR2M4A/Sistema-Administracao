from enum import Enum
from http import HTTPStatus
from werkzeug.security import generate_password_hash


from models import User
from utils import RegexPatterns
from extensions import db

import flask_login


class AuthResponses(Enum):
    """
    Centralizes all possible responses for the Auth blueprint.
    Each member holds a tuple: (content, status_code)
    """

# Respostas do Signin
    CHECK_CREDENTIALS = (
        {
            "authenticated": False,
            "status": "check_credentials",
            "redirect": None,
            "msg": "Credenciais inválidas!"
        },
        HTTPStatus.UNAUTHORIZED
    )

    BLOCKED = (
        {
            "authenticated": False,
            "status": "blocked",
            "redirect": None,
            "msg": "Conta bloqueada!"
        },
        HTTPStatus.FORBIDDEN
    )

    AUTHENTICATED = (
        {
            "authenticated": True,
            "status": "authenticated",
            "redirect": "/system/"
        },
        HTTPStatus.OK
    )

    INVALID_USERNAME = (
        {"msg": "Nome de usuário inválido!"},
        HTTPStatus.UNAUTHORIZED
    )

    PASS_MISMATCH = (
        {"msg": "Senhas não conferem!"},
        HTTPStatus.BAD_REQUEST
    )

    USER_CREATED = (
        {"msg": "Usuário criado com sucesso!"},
        HTTPStatus.CREATED
    )

    USER_ALREADY_EXISTS = (
        {"msg": "Usuário já existente!"},
        HTTPStatus.BAD_REQUEST
    )


    def build(self, **kwargs):
        """
        Builds and returns a Flask response (JSON tuple)
        based on the enum's value.
        """
        content, status = self.value

        # Para objetos json
        data = content.copy()
        data.update(kwargs)
        return data, status


class AuthService:
    """Handles user authentication and registration logic."""

    @classmethod
    def signup(cls, username: str, pass1: str, pass2, is_admin: bool):
        """
        Validates new user data, creates the user, and commits to the DB.
        """

        username = username.lower()

        if not cls.is_valid_username(username):
            return AuthResponses.INVALID_USERNAME.build()

        if User.find_by_username(username):
            return AuthResponses.USER_ALREADY_EXISTS.build()

        if pass1 != pass2:
            return AuthResponses.PASS_MISMATCH.build()

        password_hash = generate_password_hash(pass1)

        user = User.create(username, password_hash, is_admin)
        db.session.add(user)
        db.session.commit()

        return AuthResponses.USER_CREATED.build()


    @classmethod
    def signin(cls, username: str, password: str) -> dict:
        """
        Validates user credentials and handles the login session.
        """

        user = User.find_by_username(username)

        if not user:
            return AuthResponses.CHECK_CREDENTIALS.build()

        if not user.check_password(password):
            if not cls.handle_failed_attempt(user):
                return AuthResponses.BLOCKED.build()

            return AuthResponses.CHECK_CREDENTIALS.build()

        flask_login.logout_user()
        flask_login.login_user(user)
        user.misses = 0
        db.session.commit()

        return AuthResponses.AUTHENTICATED.build()


    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Validates the username format."""

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
        """
        Increments failed attempts and blocks the user if necessary.
        Returns `False` if the user is now blocked, `True` otherwise.
        """

        user.misses += 1

        if user.misses >= 3:
            user.is_active = False

        db.session.commit()
        return user.is_active
