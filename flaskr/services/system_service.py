import re
from math import ceil
from enum import Enum
from datetime import datetime
from http import HTTPStatus
from typing import Union, Optional, List

# Bibliotecas de terceiros
from validate_docbr import CPF
from flask import render_template, url_for, redirect, session, Request

# Imports do seu projeto
from models import Client, Entrance
from extensions import db
from utils import *


class SystemResponses(Enum):

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
        {"msg": "O cliente não existe!"}, HTTPStatus.NOT_FOUND
    )

    CLIENT_UPDATED = (
        {"msg": "Cliente atualizado!"}, HTTPStatus.OK
    )

    CLIENT_FOUND = (
        {"msg": "Cliente encontrado!"}, HTTPStatus.OK
    )

    REDIRECT_TO_CLIENTS = ("system.system_get", HTTPStatus.OK)

    RENDER_CLIENTS = ("system/system.html", HTTPStatus.OK)

    def build(self, **kwargs):
        """Retorna a resposta com dados adicionais ao dicionário."""
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


class SystemService:
    """Classe responsável por tratar da gravação e leitura de clientes
    no banco de dados, referente à rota system.
    """

    CPF_VALIDATOR = CPF()

    VALIDATORS = {
        "name": "is_valid_name",
        "rg": "is_valid_rg",
        "cpf": "is_valid_cpf",
        "phone-number": "is_valid_phone",
        "birth-date": "is_valid_birth_date"
    }


    @classmethod
    def handle_client_creation(cls, data: dict) -> Client:
        """Instancia e armazena um cliente e sua entrada."""

        errors = cls.validate_all(data)

        if errors:
            return SystemResponses.INVALID_DATA.build(errors=errors)

        identifier = data.get("cpf") or data.get("rg")
        if cls.find_client(identifier):

            return SystemResponses.CLIENT_EXISTS.value

        client = Client.create(*data.values())
        entrance = Entrance.create(client)

        db.session.add(client)
        db.session.add(entrance)
        db.session.commit()

        return SystemResponses.CLIENT_CREATED.value

    @classmethod
    def handle_client_update(cls, data: dict) -> Client:

        client_id = data.get("client-id")

        if not client_id.isdigit():
            return SystemResponses.CLIENT_NOT_EXISTS.value

        client = cls.find_client(int(client_id))

        if not client:
            return SystemResponses.CLIENT_NOT_EXISTS.value

        pressed_bt = data.get("bt")

        if pressed_bt == 'edit':
            phone_number = sanitize(data.get("phone-number"))

            if not cls.is_valid_phone(phone_number):
                return SystemResponses.INVALID_DATA.build(phone_number=phone_number)

            setattr(client, "phone_number", phone_number)
            db.session.commit()

        entrance = Entrance.create(client)
        db.session.add(entrance)
        db.session.commit()
        return SystemResponses.CLIENT_UPDATED.value

    @classmethod
    def handle_client_search(cls, data: dict):

        data = sanitize_many(data)
        search_by, value = data.get("search"), data.get("search-bar")

        validator = getattr(cls, f"is_valid_{search_by}")

        if not validator(value):
            return SystemResponses.INVALID_DATA.value

        client = cls.find_client(value)

        if not client:
            return SystemResponses.CLIENT_NOT_EXISTS.value

        client = cls.mask_client_info(client)
        client.update({"status": "success"})

        return client


    @staticmethod
    def handle_clients_render(data: Request, page_id: str):
        """Carrega a página principal do sistema."""

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
        return SystemResponses.RENDER_CLIENTS.build(client_entries=client_entries)


    @staticmethod
    def find_client(value: Union[str, int]) -> Optional[Client]:
        """Busca pelo cliente no banco de dados e o retorna."""

        for func in (Client.find_by_id, Client.find_by_rg, Client.find_by_cpf):

            client = func(value)
            if client:
                return client

        return None


    @staticmethod
    def mask_client_info(client: Union[Client, dict]) -> dict:
        """Retorna o cliente com suas informações sensíveis mascaradas."""

        client = model_to_dict(client)

        client["cpf"] = mask_cpf(client.get("cpf"))
        client["rg"] = mask_rg(client.get("rg"))
        client["phone_number"] = mask_phone_number(client.get("phone_number"))

        return client


    @classmethod
    def get_clients_interval(cls, page_id: int, per_page: int = 20):
        """Retorna a lista de clientes com base na págína que o usuário
        está atualmente, e a quantidade de clientes que são mostradas
        simultaneamente."""

        entrances = Entrance.find_all()
        total_entrances = Entrance.count()

        total_pages = ceil(total_entrances / per_page)
        page_id = max(1, min(page_id, total_pages))

        start_index = per_page * (page_id - 1)
        end_index = min(start_index + per_page, total_entrances)

        clients = []

        for entrance in entrances[start_index:end_index]:
            client = entrance.client
            client = cls.mask_client_info(client)
            clients.append((client, entrance))

        return clients, page_id


    @classmethod
    @input_sanitized
    def is_valid_name(cls, user_input: str) -> bool:
        """Valida o nome."""
        return bool(user_input)


    @classmethod
    @input_sanitized
    def is_valid_rg(cls, user_input: str) -> bool:
        """Valida o rg."""
        return bool(user_input)


    @classmethod
    @input_sanitized
    def is_valid_cpf(cls, user_input: str) -> bool:
        """Valida o cpf."""
        return bool(user_input) and cls.CPF_VALIDATOR.validate(user_input)


    @classmethod
    @input_sanitized
    def is_valid_phone(cls, user_input: str) -> bool:
        """Valida o número de telefone."""

        pattern = RegexPatterns.PHONE_NUMBER.value
        is_valid = pattern.fullmatch(user_input)

        return bool(is_valid and user_input)


    @classmethod
    @input_sanitized
    def is_valid_birth_date(cls, user_input: str) -> bool:
        """Valida a data de nascimento."""

        pattern = RegexPatterns.BIRTH_DATE.value
        is_valid = re.fullmatch(pattern, user_input)

        if not is_valid or not user_input:
            return False

        day, month, year = map(int, [user_input[:2], user_input[3:5], user_input[6:8]])

        if month < 1 or month > 12:
            return False

        if day < 1 or day > get_days_in_month(month, year):
            return False

        if year > datetime.today().year:
            return False

        if to_datetime(user_input) > datetime.today():
            return False

        return True


    @classmethod
    def validate_all(cls, data: dict) -> List[str]:
        """Valida todos os campos com as funções de validação."""

        errors = []
        sanitized = sanitize_many(data)

        for key, validator_name in cls.VALIDATORS.items():

            function = getattr(cls, validator_name)
            is_valid = function(sanitized.get(key, ""))

            if not is_valid:
                errors.append(key)

        return errors
