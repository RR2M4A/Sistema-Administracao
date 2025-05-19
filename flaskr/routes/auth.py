from flask import Blueprint, render_template, request, session, url_for
from services.auth_service import AuthService
from models.user import User
from extensions.login_manager import login_manager
from http import HTTPStatus
from utils.decorators import no_account


auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)


@auth.get("/signin/")
def signin_get():
    """Carrega a página de sign in."""


    return render_template("signin.html")


@auth.post("/signin/")
def signin_post():
    """Lida com requisições do tipo POST na página de sign in."""

    req = request.get_json()
    username = req["username"]
    password = req["password"]

    res = AuthService.authenticate_user(username, password)

    if not res.get("is_active"):
        return {"authenticated": False, 
                "is_active": False, 
                "redirect": None}

    if not res.get("authenticated"):
        return {"authenticated": False, 
                "is_active": True, 
                "redirect": None}

    return {"authenticated": True, 
            "is_active": True, 
            "redirect": url_for("system.system_get")}


@auth.get("/")
@auth.get("/signup/")
@no_account
def signup_get():
    """Carrega a página de signup."""
    
    return render_template("signup.html")


@auth.post("/")
@auth.post("/signup/")
@no_account
def signup_post():
    """Lida com requisições do tipo POST na página de sign up."""
    
    req = request.get_json()
    username = req.get("username")
    pass1 = req.get("first-password")
    pass2 = req.get("second-password")

    if not AuthService.is_valid_username(username):
        return {"status": "error"}, HTTPStatus.BAD_REQUEST
    
    if not AuthService.is_same_password(pass1, pass2):
        return {"status": "error"}, HTTPStatus.UNAUTHORIZED

    AuthService.create_user(username, pass1, is_admin=True)
    
    return {"status": "success"}, HTTPStatus.CREATED
