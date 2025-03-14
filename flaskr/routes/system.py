from flask import Blueprint, render_template, request
from utils.decorators import login_required
from services.validation_service import ValidationService
from services.system_service import SystemService
from http import HTTPStatus


system = Blueprint("system", __name__)


@system.get("/system/")
@login_required
def system_get():
    """Carrega a página principal do sistema."""

    return render_template("system.html")


@system.post("/system/add_client")
@login_required
def system_add_client():
    """Lida com requisições do tipo POST na página principal do sistema."""
    
    req = request.get_json()
    errors = ValidationService.validate_all(req)

    if errors:
        return {
            "status": "error",
            "errors": errors
        }, HTTPStatus.BAD_REQUEST

    client = SystemService.create_client(req)
    SystemService.create_entrance(client)

    return {"status": "success"}, HTTPStatus.CREATED


@system.post("/system/search_client")
@login_required
def system_search_client():
    """Lida com requisições do tipo POST na página principal do sistema."""
    
    req = request.get_json()
    cpf = req.get("cpf")
    _, is_valid = ValidationService.validate_cpf(cpf)

    if not is_valid:
        return {"status": "error"}, HTTPStatus.BAD_REQUEST

    client = SystemService.find_client(cpf)

    if not client:
        return {"status": "error"}, HTTPStatus.NOT_FOUND


    