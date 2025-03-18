from flask import session, redirect, url_for
from functools import wraps
from utils.sanitizers import sanitize

def login_required(f):
    """Exige que o usuário esteja logado para acessar as rotas."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if "id" not in session:
            return redirect(url_for("signin.signin_get"))
        return f(*args, **kwargs)

    return wrapper


def input_sanitized(f):
    """Retorna o input sanitizado."""

    @wraps(f)
    def wrapper(self, input, *args, **kwargs):
        input = sanitize(str(input))
        return f(self, input, *args, **kwargs)

    return wrapper