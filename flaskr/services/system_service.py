import re
from math import ceil
from enum import Enum
from datetime import datetime
from http import HTTPStatus
from typing import Union, Optional, List

from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from validate_docbr import CPF
from flask import render_template, url_for, redirect, session, Request

from models import Client, Entrance, DEPARTMENTS
from extensions import db
from utils import *


class SystemResponses(Enum):
    """
    Centralizes all possible responses for the System blueprint.
    Each member holds a tuple: (content, status_code)
    """

    CLIENT_CREATED = (
        {"msg": "Cliente criado com sucesso!"}, HTTPStatus.CREATED
    )

    INVALID_DATA = (
        {"msg": "Erros encontrados!"}, HTTPStatus.BAD_REQUEST
    )

    CLIENT_EXISTS = (
        {"msg": "O cliente já existe!"}, HTTPStatus.CONFLICT
    )

    CLIENT_NOT_EXISTS = (
        {"msg": "Cliente não encontrado, siga com o cadastro."}, HTTPStatus.NOT_FOUND
    )

    CLIENT_UPDATED = (
        {"msg": "Nova entrada registrada e telefone atualizado!"}, HTTPStatus.OK
    )

    CLIENT_FOUND = (
        {"msg": "Cliente já cadastrado."}, HTTPStatus.OK
    )

    CLIENT_DATA_MISMATCH = (
        {"msg": "Este CPF já está cadastrado com dados diferentes!"},
        HTTPStatus.CONFLICT
    )

    REDIRECT_TO_CLIENTS = ("system.system_get", HTTPStatus.OK)

    RENDER_CLIENTS = ("system/system.html", HTTPStatus.OK)

    def build(self, **kwargs):
        """Retorna a resposta com dados adicionais ao dicionário."""
        content, status = self.value

        # For template names or redirect
        if isinstance(content, str):

            # Template
            if content.endswith(".html"):
                return render_template(content, **kwargs)

            return redirect(url_for(content, **kwargs))

        # For JSON objects
        data = content.copy()
        data.update(kwargs)
        return data, status


class SystemService:
    """Handles business logic for client registration and entrances."""

    CPF_VALIDATOR = CPF()

    VALIDATORS = {
        "name": "is_valid_name",
        "rg": "is_valid_rg",
        "cpf": "is_valid_cpf",
        "birth-date": "is_valid_birth_date",
        "department": "is_valid_department"
    }

    MAX_AGE = 130


    @classmethod
    @sanitize_all
    def handle_client_creation(cls, data: dict) -> Client:
        """
        Validates, creates and updates a client.
        - If it's a new client, then a new client and their entrance is created.
        - If the client exists, their phone is updated (if phone was changed) and a new entrace is created.
        """

        errors = cls.validate_all(data)
        if errors:
            return SystemResponses.INVALID_DATA.build(errors=errors)

        client = Client.find_by_cpf(data.get("cpf"))

        try:
            if client:
                new_phone_number = data.get("phone-number")

                if (client.name != data.get("name") or
                    client.rg != data.get("rg") or
                    client.birth_date != data.get("birth-date")):

                    return SystemResponses.CLIENT_DATA_MISMATCH.build()

                if client.phone_number != new_phone_number:
                    client.phone_number = new_phone_number

                entrance = Entrance.create(client, department=data.get('department'))
                db.session.add(entrance)

            else:
                new_client = Client.create(
                    name=data.get("name"),
                    rg=data.get("rg"),
                    cpf=data.get("cpf"),
                    phone_number=data.get("phone-number"),
                    birth_date=data.get("birth-date")
                )

                entrance = Entrance.create(new_client, department=data.get('department'))
                db.session.add(new_client)
                db.session.add(entrance)

            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            return SystemResponses.CLIENT_EXISTS.build(
                msg="Conflito de dados. O CPF ou RG já pode estar cadastrado."
            )

        if client:
            return SystemResponses.CLIENT_UPDATED.build()
        else:
            return SystemResponses.CLIENT_CREATED.build()


    @classmethod
    @sanitize_all
    def get_client_entrances(cls, data: dict):
        """Searches for a client and returns all their entrances."""

        SEARCH_VALIDATORS = {
            "cpf": cls.is_valid_cpf,
            "rg": cls.is_valid_rg
        }

        search_by, value = data.get("search"), data.get("search-bar")

        validator = SEARCH_VALIDATORS.get(search_by)

        if not validator or not validator(value):
            return SystemResponses.INVALID_DATA.build(errors=[search_by or "search"])


        client = cls.find_client(value)

        if not client:
            return SystemResponses.CLIENT_NOT_EXISTS.build()

        entrances = Entrance.find_by_client(client.id)
        client_info = mask_client_info(client)

        results = [{
            **client_info,
            "department": entrance.department,
            "date": entrance.entrance.strftime("%d/%m/%Y"),
            "time": entrance.entrance.strftime("%H:%M:%S")
        } for entrance in entrances]

        return SystemResponses.CLIENT_FOUND.build(results=results)


    @classmethod
    @sanitize_all
    def get_client_info(cls, data: dict):
        """Looks for a client in the DB and returns their info."""

        client = cls.find_client(data.get('cpf'))

        if not client:
            return SystemResponses.CLIENT_NOT_EXISTS.build()

        return SystemResponses.CLIENT_FOUND.build(client_info=model_to_dict(client))


    @staticmethod
    def handle_clients_render(data: Request, page_id: str):
        """Loads the main system page with paginated clients."""

        page_mov = data.args.get("arrow")

        if page_mov:
            previous_page = session.get("page_id", 1)
            next_page = previous_page + 1 if page_mov == "right" else previous_page - 1

            return SystemResponses.REDIRECT_TO_CLIENTS.build(page_id=next_page)

        if not page_id.isdigit():
            return SystemResponses.REDIRECT_TO_CLIENTS.build(page_id=1)

        page_id = int(page_id)
        client_entries, new_page_id = SystemService.get_clients_interval(page_id)

        if page_id != new_page_id:
            return SystemResponses.REDIRECT_TO_CLIENTS.build(page_id=new_page_id)

        session["page_id"] = new_page_id
        return SystemResponses.RENDER_CLIENTS.build(
            client_entries=client_entries,
            departments = DEPARTMENTS,
        )


    @staticmethod
    def find_client(value: Union[str, int]) -> Optional[Client]:
        """Finds a client by ID, RG, or CPF."""

        for func in (Client.find_by_id, Client.find_by_rg, Client.find_by_cpf):

            client = func(value)
            if client:
                return client

        return None


    @staticmethod
    def get_clients_interval(page_id: int, per_page: int = 20):
        """
        Returns a paginated list of clients for the given page.
        """

        total_entrances = Entrance.count()

        if total_entrances == 0:
            return [], 1

        total_pages = ceil(total_entrances / per_page)
        page_id = max(1, min(page_id, total_pages))

        offset = per_page * (page_id - 1)

        paginated_query = db.select(Entrance).order_by(
            Entrance.entrance.desc()
        ).options(
            joinedload(Entrance.client)
        ).offset(offset).limit(per_page)

        entrances = db.session.scalars(paginated_query).all()

        clients = []
        for entrance in entrances:
            client_data = mask_client_info(entrance.client)
            clients.append((client_data, entrance))

        return clients, page_id


    @staticmethod
    def is_valid_name(user_input: str) -> bool:
        """Checks if the name is valid."""
        return bool(user_input.strip())


    @staticmethod
    def is_valid_rg(user_input: str) -> bool:
        """Checks if the RG is valid."""
        return bool(user_input.strip())


    @classmethod
    def is_valid_cpf(cls, user_input: str) -> bool:
        """Checks if the CPF is valid."""
        return bool(user_input) and cls.CPF_VALIDATOR.validate(user_input)


    @staticmethod
    def is_valid_phone(user_input: str) -> bool:
        """Checks if the phone number is valid."""

        if not user_input:
            return True

        pattern = RegexPatterns.PHONE_NUMBER.value
        is_valid = pattern.fullmatch(user_input)

        return is_valid and user_input


    @classmethod
    def is_valid_birth_date(cls, user_input: str) -> bool:
        """Checks if the birth date is valid."""

        pattern = RegexPatterns.BIRTH_DATE.value
        is_valid = re.fullmatch(pattern, user_input)

        if not is_valid or not user_input:
            return False

        try:
            limit_year = datetime.today().year - cls.MAX_AGE
            lower_date = datetime(limit_year, 1, 1)

            day, month, year = map(int, user_input.split('/'))
            parsed_date = datetime(year, month, day)

            if parsed_date > datetime.today() or parsed_date < lower_date:
                return False

            return True
        except ValueError:
            return False


    @staticmethod
    def is_valid_department(department: str):
        """Checks if the department is valid."""
        return department in DEPARTMENTS


    @classmethod
    def validate_all(cls, data: dict) -> List[str]:
        """
        Validates all fields from a pre-sanitized dict.
        """

        errors = []

        for key, validator_name in cls.VALIDATORS.items():
            function = getattr(cls, validator_name)
            is_valid = function(data.get(key, ""))

            if not is_valid:
                errors.append(key)

        phone_number = data.get("phone-number", "")
        if not cls.is_valid_phone(phone_number):
            errors.append("phone-number")

        return errors
