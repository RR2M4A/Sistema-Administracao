from flask import session, redirect, url_for, abort
from functools import wraps
from utils.sanitizers import sanitize
from models.user import User
from models.client import Client
from flask_login import login_required, current_user

def input_sanitized(f):
    """Retorna o input sanitizado."""

    @wraps(f)
    def wrapper(self, input, *args, **kwargs):
        input = sanitize(str(input))
        return f(self, input, *args, **kwargs)

    return wrapper

def no_account(f):
    """Utilizado para quando o usuário acessa o sistema pela primeira vez."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if User.has_any() or Client.has_any():
            return redirect(url_for("auth.signin_get"))
        return f(*args, **kwargs)

    return wrapper

def access_required(f):
    """Exige que o usuário esteja desbloqueado para acessar a rota."""

    @login_required
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_active:
            return redirect(url_for('auth.signin_get'))
        return f(*args, **kwargs)

    return wrapper


def admin_required(f):
    """Exige que o usuário tenha permissão de admin para acessar a rota."""

    @access_required
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            return abort(403)
        return f(*args, **kwargs)

    return wrapper