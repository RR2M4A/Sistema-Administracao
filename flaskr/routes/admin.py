from utils import admin_required
from services import AdminService

from flask import Blueprint, request


admin = Blueprint("admin", __name__)


@admin.get("/admin/")
@admin_required
def admin_get():
    """Treats GET requests to the /admin/ route."""

    return AdminService.handle_users_render()


@admin.post("/admin/get_info/")
@admin_required
def admin_view_info():
    """Treats POST requests to the /admin/get_info/ route to view user info."""

    req = request.get_json()
    return AdminService.handle_user_load(req)


@admin.post("/admin/edit/")
@admin_required
def admin_edit():
    """Treats POST requests to the /admin/edit/ route to edit user info."""
    req = request.get_json()
    return AdminService.handle_user_update(req)


@admin.post("/admin/new/")
@admin_required
def admin_new():
    """Treats POST requests to the /admin/new/ route to create a new user."""

    req = request.get_json()
    return AdminService.handle_user_creation(req)


@admin.post("/admin/delete/")
@admin_required
def admin_delete():
    "Treats POST requests to the /admin/delete/ route to remove a user."

    req = request.get_json()
    return AdminService.handle_user_removal(req)


@admin.post("/admin/run_reports/")
@admin_required
def admin_reports():
    "Treats POST requests to the /admin/run_reports/ route to generate reports."""

    req = request.get_json()
    return AdminService.handle_report_generation(req)
