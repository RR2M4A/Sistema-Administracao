from flask import Blueprint, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from models import User
from database import db


signin = Blueprint("signin", __name__)


@signin.get("/signin/")
def signin_get():
    """Carrega a páǵina de sign in."""

    return render_template("signin.html")


@signin.post("/signin/")
def signin_post():
    """Lida com requisições do tipo POST na página de sign in."""

    req = request.get_json()
    inputed_username = req["username"]
    inputed_password = req["password"]

    db_user = db.session.execute(
        db.select(User).where(User.username == inputed_username)
        ).scalar_one_or_none()

    if db_user and check_password_hash(db_user.password, inputed_password):
        session["id"] = db_user.id
        return {"authenticated": "true", "redirect": url_for("system.system_get")}
    
    return {"authenticated": "false"}