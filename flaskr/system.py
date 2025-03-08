from flask import Blueprint, render_template, request
from utils import login_required


system = Blueprint("system", __name__)


@system.get("/system/")
@login_required
def system_get():
    """Carrega a página principal do sistema."""

    return render_template("system.html")


@system.post("/system/")
@login_required
def system_post():
    """Lida com requisições do tipo POST na página principal do sistema."""
    
    res = request.get_json()
    for i in res:
        print(i)

    return render_template("system.html")
    