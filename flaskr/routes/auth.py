from flask import Blueprint, render_template, request
from services import AuthService
from models import User
from extensions import login_manager
from utils import no_account


auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)


@auth.get("/signin/")
def signin_get():
    """Loads the sign in page."""

    return render_template("auth/signin.html")


@auth.post("/signin/")
def signin_post():
    """Treats the POST requests to the /signin/ route."""

    req = request.get_json()
    username = req["username"]
    password = req["password"]

    return AuthService.signin(username, password)


@auth.get("/")
@auth.get("/signup/")
@no_account
def signup_get():
    """Loads the sign up page."""

    return render_template("auth/signup.html")


@auth.post("/")
@auth.post("/signup/")
@no_account
def signup_post():
    """Treats the POST requests to the /signup/ route."""

    req = request.get_json()
    username = req.get("username")
    pass1 = req.get("first-password")
    pass2 = req.get("second-password")

    return AuthService.signup(username, pass1, pass2, True)
