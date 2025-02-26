from flask import session, redirect, url_for
from functools import wraps

def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        if not "id" in session:
            return redirect(url_for("auth.signin_get"))
        return f(*args, **kwargs)

    return wrapper