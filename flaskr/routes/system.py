from flask import Blueprint, request
from utils import access_required
from services import SystemService


system = Blueprint("system", __name__)


@system.get("/system/")
@system.get("/system/<page_id>")
@access_required
def system_get(page_id = "1"):
    """Loads the system main page, with clients listed paginated."""

    req = request
    return SystemService.handle_clients_render(req, page_id)


@system.post("/system/add_client/")
@access_required
def system_add_client():
    """Adds a new client to the system."""

    req = request.get_json()
    return SystemService.handle_client_creation(req)


@system.post('/system/get_client_info/')
@access_required
def system_get_client_info():
    """Returns the info of a client, if found."""

    req = request.get_json()
    return SystemService.get_client_info(req)


@system.post("/system/get_client_entrances/")
@access_required
def system_get_client_entrances():
    """
    Busca um cliente (CPF ou RG) e retorna todas as suas entradas.
    É chamado pelo searchClient.js.
    """
    req = request.get_json()
    return SystemService.get_client_entrances(req)