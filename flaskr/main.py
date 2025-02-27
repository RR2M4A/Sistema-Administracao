from flask import Blueprint, render_template, request
from utils import login_required


main = Blueprint("main", __name__)


@main.get("/system/")
@login_required
def system_get():
    """Carrega a página principal do sistema."""

    return render_template("main.html")


@main.post("/system/")
@login_required
def system_post():
    """Lida com requisições do tipo POST na página principal do sistmea."""
    
    res = request.get_json()
    for i in res:
        print(i)

    return render_template("templates/main.html")
    