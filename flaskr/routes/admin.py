from utils import admin_required
from services import AdminService
from services import AuthService

from flask import Blueprint, request


admin = Blueprint("admin", __name__)


@admin.get("/admin/")
@admin_required
def admin_get():
    """Lida com o carregamento dos usuários na página."""

    return AdminService.handle_users_render()


@admin.post("/admin/")
@admin_required
def admin_view_info():
    """Retorna as informações do usuário selecionado."""

    req = request.get_json()
    return AdminService.handle_user_load(req)


@admin.post("/admin/edit/")
@admin_required
def admin_edit():
    """Lida com as edições dos atributos de admin."""

    req = request.form
    return AdminService.handle_user_update(req)


@admin.post("/admin/new/")
@admin_required
def admin_new():
    """Lida com a criação de novos usuários."""

    req = request.get_json()
    username = req.get("popup__username")
    pass1 = req.get("first-pass")
    pass2 = req.get("second-pass")
    is_admin = req.get("is-admin") == 'true'

    return AuthService.signup(username, pass1, pass2, is_admin)


@admin.post("/admin/delete/")
@admin_required
def admin_delete():
    "Lida com a remoção de um usuário."

    req = request.get_json()
    return AdminService.handle_user_removal(req)


@admin.post("/admin/run_reports/")
@admin_required
def admin_reports():
    "Responsável por gerar o relatório de clientes."

    req = request.get_json()
    return AdminService.handle_report_generation(req)
