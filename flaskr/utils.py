from flask import session, redirect, url_for
from functools import wraps

def login_required(f):
    """Exige que o usuário esteja logado para acessar as rotas."""

    @wraps(f)
    def wrapper(*args, **kwargs):

        if "id" not in session:
            return redirect(url_for("signin.signin_get"))
        return f(*args, **kwargs)

    return wrapper