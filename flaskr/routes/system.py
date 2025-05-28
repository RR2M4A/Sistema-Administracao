from flask import Blueprint, render_template, request, redirect, url_for, session
from utils.decorators import access_required
from services.system_service import SystemService


system = Blueprint("system", __name__)


@system.get("/system/")
@system.get("/system/<page_id>")
@access_required
def system_get(page_id = "1"):
    """Carrega a página principal do sistema."""

    req = request
    return SystemService.handle_clients_render(req, page_id)


@system.post("/system/add_client")
@access_required
def system_add_client():
    """Recebe os dados do cliente via POST, os valida e cria o cliente."""

    req = request.get_json()
    return SystemService.handle_client_creation(req)


@system.post("/system/search_client")
@access_required
def system_search_client():
    """Busca o cliente no sistema, através do cpf informado."""

    req = request.get_json()
    return SystemService.handle_client_search(req)


@system.post("/system/update_client")
@access_required
def system_update_client():
    """Atualiza o nº de telefone ou a entrada do cliente."""

    req = request.get_json()
    return SystemService.handle_client_update(req)