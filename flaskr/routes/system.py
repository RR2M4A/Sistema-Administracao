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


@system.post("/system/add_client")
@access_required
def system_add_client():
    """Adds a new client to the system."""

    req = request.get_json()
    return SystemService.handle_client_creation(req)


@system.post("/system/search_client")
@access_required
def system_search_client():
    """Searches for a client in the system."""

    req = request.get_json()
    return SystemService.handle_client_search(req)


@system.post("/system/update_client")
@access_required
def system_update_client():
    """Updates client information in the system."""

    req = request.get_json()
    return SystemService.handle_client_update(req)
