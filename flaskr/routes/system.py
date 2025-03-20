from flask import Blueprint, render_template, request
from utils.decorators import login_required
from services.system_service import SystemService
from services.validation_service import ValidationService
from http import HTTPStatus
from utils.sanitizers import sanitize_many
from utils.masks import mask_cpf, mask_rg, mask_phone_number
from utils.date_utils import to_datetime


system = Blueprint("system", __name__)


@system.get("/system/")
@login_required
def system_get():
    """Carrega a página principal do sistema."""

    clients = SystemService.get_masked_clients()
    return render_template("system.html", clients=clients)


@system.post("/system/add_client")
@login_required
def system_add_client():
    """Recebe os dados do cliente via POST, os valida e cria o cliente."""
    
    req = sanitize_many(request.get_json())
    errors = ValidationService.validate_all(req)

    if errors:
        return {
            "status": "error",
            "errors": errors
        }, HTTPStatus.BAD_REQUEST
    
    if SystemService.find_client(req["cpf"], req["rg"]):
        return {"status": "error"}, HTTPStatus.CONFLICT

    client = SystemService.create_client(req)
    SystemService.create_entrance(client)

    return {"status": "success"}, HTTPStatus.CREATED


@system.post("/system/search_client")
@login_required
def system_search_client():
    """Busca o cliente no sistema, através do cpf informado."""
    
    req = sanitize_many(request.get_json())
    search_by, value = req.get("search"), req.get("search-bar")

    validator = getattr(ValidationService, f"validate_{search_by}")
    
    _, is_valid = validator(value)
    
    if not is_valid:
        return {"status": "error"}, HTTPStatus.BAD_REQUEST

    client = SystemService.find_client(value)

    if not client:
        return {"status": "error"}, HTTPStatus.NOT_FOUND

    client = SystemService.mask_client_info(client)
    client.update({"status": "success"})

    return client, HTTPStatus.OK