from flask import Blueprint, render_template, request, session, url_for, redirect
from utils.sanitizers import sanitize_many
from http import HTTPStatus
from utils.converters import model_to_dict
from utils.decorators import admin_required
from extensions.database import db
from services.admin_service import AdminService

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
    return AdminService.handle_admin_update(req)