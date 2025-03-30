from flask import session, redirect, url_for
from functools import wraps
from utils.sanitizers import sanitize
from models.user import User
from models.client import Client

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


def no_account(f):
    """Utilizado para quando o usuário acessa o sistema pela primeira vez."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if User.has_any() or Client.has_any():
            print("Entrou no if")
            return redirect(url_for("auth.signin_get"))
        
        print("Passou direto")
        return f(*args, **kwargs)
    
    return wrapper