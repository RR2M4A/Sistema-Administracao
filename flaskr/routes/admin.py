from flask import Blueprint, render_template, request, session, url_for
from models.user import User
from utils.sanitizers import sanitize_many
from http import HTTPStatus
from utils.converters import model_to_dict
from utils.decorators import admin_required


admin = Blueprint("admin", __name__)


@admin_required
@admin.get("/admin/")
def admin_get():

    users = User.find_all()
    print(users)
    return render_template("admin.html", users=users)
    


@admin_required
@admin.post("/admin/")
def admin_view_info():

    req = sanitize_many(request.get_json())
    id = req.get("id")

    user = model_to_dict(User.find_by_id(id))
    user.pop("password_hash")
    return user, HTTPStatus.OK


@admin_required
@admin.post("/admin/")
def admin_edit():

    req = sanitize_many(request.get_json())
    id = req.get("id")

    user = model_to_dict(User.find_by_id(id))
    user.pop("password_hash")
    return user, HTTPStatus.OK