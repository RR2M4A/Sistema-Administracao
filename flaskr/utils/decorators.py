from flask import redirect, url_for, abort
from functools import wraps
from models.user import User
from models.client import Client
from flask_login import login_required, current_user
from utils import sanitize_many


def no_account(f):
    """
    Used for the first-time setup route.
    If any user or client exists, redirects to the login page.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if User.has_any() or Client.has_any():
            return redirect(url_for("auth.signin_get"))
        return f(*args, **kwargs)

    return wrapper

def access_required(f):
    """
    Requires the user to be logged in (@login_required) AND
    to be an active (not blocked) user.
    """

    @login_required
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_active:
            return redirect(url_for('auth.signin_get'))
        return f(*args, **kwargs)

    return wrapper


def admin_required(f):
    """
    Requires the user to have admin permissions.
    This decorator stacks on top of @access_required.
    """

    @access_required
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            return abort(403)
        return f(*args, **kwargs)

    return wrapper


def sanitize_all(f):
    """
    Automatically sanitizes the data that comes from the FrontEnd.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):

        data = kwargs.get('data')

        if isinstance(data, dict):
            kwargs["data"] = sanitize_many(data)

        elif args and len(args) > 1 and isinstance(args[1], dict):
            new_args = list(args)
            new_args[1] = sanitize_many(args[1])
            args = tuple(new_args)

        return f(*args, **kwargs)

    return wrapper