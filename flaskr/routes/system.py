from flask import Blueprint, render_template, request
from utils.decorators import login_required
from services.validation_service import ValidationService


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
    
    req = request.get_json()
    validation_result = ValidationService.validate_all(req)

    