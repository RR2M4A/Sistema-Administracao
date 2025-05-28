from enum import Enum
from flask import render_template, url_for, redirect
from http import HTTPStatus
from models.user import User
from utils.sanitizers import sanitize_many
from utils.converters import model_to_dict
from extensions.database import db

class AdminResponses(Enum):

    RENDER_USERS = ("admin.html", HTTPStatus.OK)
    REDIRECT_TO_USERS = ("admin.admin_get", HTTPStatus.OK)

    LOAD_USER = ({"msg": "Usuário carregado com sucesso!"}, HTTPStatus.OK)
    USER_NOT_FOUND = ({"msg": "Usuário não encontrado!"}, HTTPStatus.NOT_FOUND)


    def build(self, **kwargs):
        content, status = self.value

        # Para nomes de template ou redirecionamentos
        if isinstance(content, str):

            # Template
            if content.endswith(".html"):
                return render_template(content, **kwargs)

            return redirect(url_for(content, **kwargs))

        # Para objetos json
        data = content.copy()
        data.update(kwargs)
        return data, status


class AdminService:


    @staticmethod
    def handle_users_render():
        """Carrega os usuários na tela."""

        users = User.find_all()
        return AdminResponses.RENDER_USERS.build(users=users)


    @staticmethod
    def handle_user_load(data: dict):
        """Carrega as informações de um único usuário na tela."""

        data = sanitize_many(data)
        user = model_to_dict(User.find_by_id(data.get('id')))

        return AdminResponses.LOAD_USER.build(user=user)


    @staticmethod
    def handle_admin_update(data: dict):
        """Lida com as edições do usuário selecionado."""

        admin_val = True if data.get("is-admin") == 'true' else False
        blocked_val = True if data.get("is-blocked") == 'true' else False
        user = User.find_by_id(data.get('id'))

        if not user:
            return AdminResponses.REDIRECT_TO_USERS.build()

        user.is_admin = admin_val
        user.is_blocked = blocked_val
        db.session.commit()

        return AdminResponses.REDIRECT_TO_USERS.build()

