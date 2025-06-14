from enum import Enum
from flask import render_template, url_for, redirect, send_file
from http import HTTPStatus
from models.user import User
from utils.sanitizers import sanitize_many
from utils.converters import model_to_dict
from extensions.database import db
from utils.regex import RegexPatterns
from services.auth_service import AuthService
from flask_login import current_user
from models.client import Client
from models.entrance import Entrance
import tempfile
from datetime import datetime
from sqlalchemy import and_
import pandas as pd


class AdminResponses(Enum):

    RENDER_USERS = ("admin/admin.html", HTTPStatus.OK)
    REDIRECT_TO_USERS = ("admin.admin_get", HTTPStatus.OK)

    LOAD_USER = (
        {"msg": "Usuário carregado com sucesso!"},
        HTTPStatus.OK
    )

    USER_NOT_FOUND = (
        {"msg": "Usuário não encontrado!"},
        HTTPStatus.NOT_FOUND
    )

    USER_DELETED = (
        {"msg": "Usuário excluído com sucesso!"},
        HTTPStatus.NO_CONTENT
    )

    USER_IS_LOGGED_IN = (
        {"msg": "O usuário está logado! Operação cancelada!"},
        HTTPStatus.FORBIDDEN
    )

    DATA_NOT_FOUND = (
        {"msg": "Nenhum dado encontrado para o período selecionado."},
        HTTPStatus.NOT_FOUND
    )

    INVALID_DATA_TYPE = (
        {"msg": "Datas inválidas!"},
        HTTPStatus.BAD_REQUEST
    )


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
    def handle_user_update(data: dict):
        """Lida com as edições do usuário selecionado."""

        is_admin = True if data.get("is-admin") == 'true' else False
        is_active = True if data.get("is-active") == 'true' else False
        user = User.find_by_id(data.get('id'))

        if not user:
            return AdminResponses.REDIRECT_TO_USERS.build()

        user.is_admin = is_admin
        user.is_active = is_active
        db.session.commit()

        return AdminResponses.REDIRECT_TO_USERS.build()


    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Verifica se o USERNAME é válido."""

        pattern = RegexPatterns.USERNAME.value

        if not isinstance(username, str):
            return False

        if not username:
            return False

        if not pattern.fullmatch(username):
            return False

        return True


    @classmethod
    def handle_user_creation(cls, data: dict):
        """Valida os dados recebidos e cria um novo usuário.

        Aqui, a classe AdminService é reutilizada, pois ela já lida com a
        criação de usuários.
        """

        # É aqui que ele cria do mesmo jeito que o AuthService

        data = sanitize_many(data)

        username = data.get("popup__username")
        pass1 = data.get("first-pass")
        pass2 = data.get("second-pass")
        is_admin = True if data.get("is-admin") == 'true' else False

        return AuthService.signup(username, pass1, pass2, is_admin)


    @classmethod
    def handle_user_removal(cls, data: dict):

        user = User.find_by_id(data.get("id"))

        if not user:
            return AdminResponses.USER_NOT_FOUND.value

        logged_user = current_user.__dict__

        if user.id == logged_user.get('id'):
            return AdminResponses.USER_IS_LOGGED_IN.value

        db.session.delete(user)
        db.session.commit()
        return AdminResponses.USER_DELETED.value


    @staticmethod
    def handle_report_generation(data: dict):

        start_date = data.get("start-date")
        final_date = data.get("final-date")

        # Converte para datetime
        try:
            start_obj = datetime.strptime(start_date, "%d/%m/%Y")
            final_obj = datetime.strptime(final_date, "%d/%m/%Y")
            final_obj = final_obj.replace(hour=23, minute=59, second=59)
        except:
            return AdminResponses.INVALID_DATA_TYPE.value

        # Busca os dados entre as datas
        result = db.session.execute(
            db.select(Client, Entrance)
            .join(Entrance, Client.id==Entrance.client_id)
            .where(and_(
                Entrance.entrance >= start_obj,
                Entrance.entrance <= final_obj))).all()


        data = []
        for client, entrance in result:
            data.append({
                "Nome": client.name,
                "CPF": client.cpf,
                "Data de Nascimento": client.birth_date,
                "Telefone": client.phone_number,
                "Entrada": entrance.entrance.strftime("%d/%m/%Y %H:%M:%S")
            })

        if not data:
            print(AdminResponses.DATA_NOT_FOUND.value)
            return AdminResponses.DATA_NOT_FOUND.value

        df = pd.DataFrame(data)

        # Cria arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        df.to_excel(temp_file.name, index=False)
        temp_file.close()

        # Envia o arquivo para download
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name="relatorio.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )