from typing import List
from enum import Enum
from http import HTTPStatus
import tempfile
from datetime import datetime
from flask import render_template, url_for, redirect, send_file
from utils import sanitize_many, model_to_dict, RegexPatterns
from extensions import db
from flask_login import current_user
from models import *
from sqlalchemy import and_
import pandas as pd
from .auth_service import AuthService


class AdminResponses(Enum):
    """
    Centralizes all possible responses for the Admin blueprint.
    Each member holds a tuple: (content, status_code)
    """

    RENDER_USERS = ("admin/admin.html", HTTPStatus.OK)
    REDIRECT_TO_USERS = ("admin.admin_get", HTTPStatus.OK)

    LOAD_USER = (
        {"msg": "Usuário carregado com sucesso!"},
        HTTPStatus.OK
    )

    USER_UPDATED_SUCCESS = (
        {"msg": "Usuário atualizado com sucesso!"},
        HTTPStatus.OK
    )

    USER_NOT_FOUND = (
        {"msg": "Usuário não encontrado!"},
        HTTPStatus.NOT_FOUND
    )

    USER_DELETED = (
        {"msg": "Usuário excluído com sucesso!"},
        HTTPStatus.OK
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
        """
        Builds and returns a Flask response based on the enum's value.
        - If content is a .html file, it renders a template.
        - If content is a string (route name), it redirects.
        - If content is a dict, it returns a JSON response.
        """

        content, status = self.value

        # For template rendering or redirection
        if isinstance(content, str):

            # Template
            if content.endswith(".html"):
                return render_template(content, **kwargs)

            return redirect(url_for(content, **kwargs))

        # For JSON responses
        data = content.copy()
        data.update(kwargs)
        return data, status


class AdminService:
    """Handles business logic for administrator actions."""

    @staticmethod
    def handle_users_render():
        """Loads the users management page with all users."""

        users = User.find_all()
        return AdminResponses.RENDER_USERS.build(users=users)


    @staticmethod
    def handle_user_load(data: dict):
        """Loads the selected user's information."""

        data = sanitize_many(data)
        user = model_to_dict(User.find_by_id(data.get('id')))

        return AdminResponses.LOAD_USER.build(user=user)


    @staticmethod
    def handle_user_update(data: dict):
        """Updates the selected user's information."""


        is_admin = data.get("is-admin") == 'true'
        is_active = data.get("is-active") == 'true'
        user = User.find_by_id(data.get('id'))

        if not user:
            return AdminResponses.USER_NOT_FOUND.build()

        if user.id == current_user.id:
            if not is_admin:
                return AdminResponses.USER_IS_LOGGED_IN.build(
                    msg="Você não pode remover sua própria permissão de administrador."
                )
            if not is_active:
                 return AdminResponses.USER_IS_LOGGED_IN.build(
                    msg="Você não pode desativar sua própria conta."
                )

        user.is_admin = is_admin
        user.is_active = is_active
        db.session.commit()

        return AdminResponses.USER_UPDATED_SUCCESS.build()


    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Validates the username format."""

        pattern = RegexPatterns.USERNAME.value

        if not isinstance(username, str):
            return False

        if not username:
            return False

        if not pattern.fullmatch(username):
            return False

        return True


    @staticmethod
    def handle_user_creation(data: dict):
        """Creates a new user in the system."""

        data = sanitize_many(data)

        form_username = data.get("username")
        form_pass1 = data.get("pass1")
        form_pass2 = data.get("pass2")
        is_admin = data.get("is-admin") == 'true'

        return AuthService.signup(
            username=form_username,
            pass1=form_pass1,
            pass2=form_pass2,
            is_admin=is_admin
        )


    @staticmethod
    def handle_user_removal(data: dict):
        """Removes a user from the system."""

        user = User.find_by_id(data.get("id"))

        if not user:
            return AdminResponses.USER_NOT_FOUND.build()

        if user.id == current_user.id:
            return AdminResponses.USER_IS_LOGGED_IN.build()

        db.session.delete(user)
        db.session.commit()
        return AdminResponses.USER_DELETED.build()


    @staticmethod
    def _fetch_report_entries(start_date: datetime, final_date: datetime):
        """Queries the database for client entrances within the date range."""

        results = db.session.execute(
            db.select(Client, Entrance)
            .join(Entrance, Client.id == Entrance.client_id)
            .where(and_(
                Entrance.entrance >= start_date,
                Entrance.entrance <= final_date
            ))).all()

        # Format data for the report
        data = []
        for client, entrance in results:
            data.append({
                "Nome": client.name,
                "CPF": client.cpf,
                "Data de Nascimento": client.birth_date,
                "Telefone": client.phone_number,
                "Entrada": entrance.entrance.strftime("%d/%m/%Y %H:%M:%S")
            })
        return data


    @staticmethod
    def _create_excel_file(data: List[dict]) -> str:
        """Creates a temporary Excel file from a list of data."""
        df = pd.DataFrame(data)

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        df.to_excel(temp_file.name, index=False)
        temp_file.close()

        return temp_file.name


    @classmethod
    def handle_report_generation(cls, data: dict):
        """Generates an Excel report of client entrances within a date range."""

        start_date = data.get("start-date")
        final_date = data.get("final-date")

        # Converts strings to datetime objects
        try:
            start_obj = to_start_of_day(start_date)
            final_obj = to_end_of_day(final_date)
        except (ValueError, TypeError):
            return AdminResponses.INVALID_DATA_TYPE.build()

        # Fetches data from the database
        entries = cls._fetch_report_entries(start_obj, final_obj)

        if not entries:
            return AdminResponses.DATA_NOT_FOUND.build()

        file_name = cls._create_excel_file(entries)

        # Sends the file as a download
        return send_file(
            file_name,
            as_attachment=True,
            download_name="relatorio.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
