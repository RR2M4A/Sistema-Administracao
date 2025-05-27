from flask import Blueprint, render_template, request, redirect, url_for, session
from utils.decorators import access_required
from services.system_service import SystemService


system = Blueprint("system", __name__)


@system.get("/system/")
@system.get("/system/<page_id>")
@access_required
def system_get(page_id = "1"):
    """Carrega a página principal do sistema."""

    # Deixar a rota enxuta

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