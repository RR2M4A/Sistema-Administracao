from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from database import db

auth = Blueprint("auth", __name__)

@auth.get("/signin/")
def signin_get():
    return render_template("signin.html")

@auth.post("/signin/")
def signin_post():

    form = request.json()
    for value in form:
        print(value)
    
    return render_template("signin.html")