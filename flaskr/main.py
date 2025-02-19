from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

main = Blueprint("main", __name__)

@main.get("/system/")
def system_get():
    return render_template("main.html")


@main.post("/system/")
def system_post():
    
    res = request.get_json()
    for i in res:
        print(i)

    print("Passou aqui")

    return render_template("templates/main.html")
    