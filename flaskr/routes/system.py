from flask import Blueprint, render_template, request, redirect, url_for, session
from utils.decorators import access_required
from services.system_service import SystemService
from services.validation_service import ValidationService
from http import HTTPStatus
from utils.sanitizers import sanitize_many, sanitize


system = Blueprint("system", __name__)


@system.get("/system/")
@system.get("/system/<page_id>")
@access_required
def system_get(page_id = "1"):
    """Carrega a página principal do sistema."""

    page_mov = request.args.get("arrow")

    if page_mov:
        previous_page = session.get("page_id", 1)
        next_page = previous_page + 1 if page_mov == "right" else previous_page - 1

        return redirect(url_for("system.system_get", page_id=next_page))
    
    if not page_id.isdigit():
        return redirect(url_for("system.system_get", page_id=1))

    page_id = int(page_id)
    client_entries, new_page_id = SystemService.get_clients_interval(page_id)

    if page_id != new_page_id:
        return redirect(url_for("system.system_get", page_id=new_page_id))
    
    session["page_id"] = new_page_id
    return render_template("system.html", client_entries=client_entries)


@system.post("/system/add_client")
@access_required
def system_add_client():
    """Recebe os dados do cliente via POST, os valida e cria o cliente."""
    
    req = sanitize_many(request.get_json())
    errors = ValidationService.validate_all(req)

    if errors:
        return {
            "status": "error",
            "errors": errors
        }, HTTPStatus.BAD_REQUEST
    
    if SystemService.find_client(req["cpf"]) or SystemService.find_client(req["rg"]):
        return {"status": "error"}, HTTPStatus.CONFLICT

    client = SystemService.create_client(req)
    SystemService.create_entrance(client)

    return {"status": "success"}, HTTPStatus.CREATED


@system.post("/system/search_client")
@access_required
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


@system.post("/system/update_client")
@access_required
def system_update_client():
    """Atualiza o nº de telefone ou a entrada do cliente."""
    
    req = request.get_json()
    pressed_bt = req.get("bt")
    client_id = req.get("client-id")

    if not client_id.isdigit():
        return {"status": "error"}, HTTPStatus.NOT_FOUND

    client_id = int(client_id)
    client = SystemService.find_client(client_id)

    if not client:
        return {"status": "error"}, HTTPStatus.NOT_FOUND

    if pressed_bt == "edit":
        field_to_edit = "phone_number"
        phone_number = sanitize(req.get("phone-number"))
        _, is_valid = ValidationService.validate_phone_number(phone_number)

        if not is_valid:
            return {"status": "error"}, HTTPStatus.BAD_REQUEST

        SystemService.update_client(client, field_to_edit, phone_number)

        return {"status": "success"}, HTTPStatus.OK

    SystemService.create_entrance(client)
    return {"status": "success"}, HTTPStatus.CREATED