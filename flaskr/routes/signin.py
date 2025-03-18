from flask import Blueprint, render_template, request, session, url_for
from services.auth_service import AuthService


signin = Blueprint("signin", __name__)


@signin.get("/signin/")
def signin_get():
    """Carrega a página de sign in."""

    return render_template("signin.html")


@signin.post("/signin/")
def signin_post():
    """Lida com requisições do tipo POST na página de sign in."""

    req = request.get_json()
    username = req["username"]
    password = req["password"]

    user = AuthService.authenticate_user(username, password)

    if user:
        session["id"] = user.id
        return {"authenticated": True, "redirect": url_for("system.system_get")}
    
    return {"authenticated": False}

