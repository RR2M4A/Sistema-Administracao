from flask import Blueprint, render_template, request, session, url_for, redirect
from models.user import User
from utils.sanitizers import sanitize_many
from http import HTTPStatus
from utils.converters import model_to_dict
from utils.decorators import admin_required
from extensions.database import db


admin = Blueprint("admin", __name__)


@admin.get("/admin/")
@admin_required
def admin_get():

    users = User.find_all()
    return render_template("admin.html", users=users)


@admin.post("/admin/")
@admin_required
def admin_view_info():

    req = sanitize_many(request.get_json())
    user = model_to_dict(User.find_by_id(req.get('id')))

    return user, HTTPStatus.OK


@admin.post("/admin/edit/")
@admin_required
def admin_edit():

    req = request.form
    admin_val = True if request.form.get("is-admin") == 'true' else False
    blocked_val = True if request.form.get("is-blocked") == 'true' else False

    user = User.find_by_id(req.get('id'))

    if not user:
        return redirect(url_for('admin.admin_get'))

    user.is_admin = admin_val
    user.is_blocked = blocked_val
    db.session.commit()

    return redirect(url_for('admin.admin_get'))