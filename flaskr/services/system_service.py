from typing import Union
from models.client import Client
from models.entrance import Entrance
from extensions.database import db
from sqlalchemy.exc import SQLAlchemyError
from utils.masks import mask_cpf, mask_rg, mask_phone_number
from utils.converters import model_to_dict
from math import ceil


class SystemService:
    """Classe responsável por tratar da gravação e leitura de clientes
    no banco de dados, referente à rota system.
    """

    @staticmethod
    def create_client(data: dict) -> Client:
        """Cria e retorna um cliente."""

        try:
            return Client.create(data)
        except SQLAlchemyError:
            db.rollback()


    @staticmethod
    def create_entrance(client: Client) -> Entrance:
        """Cria e retorna uma entrada."""

        try:
            return Entrance.create(client)
        except SQLAlchemyError:
            db.rollback()


    @staticmethod
    def find_client(value) -> Client:
        """Busca pelo cliente no banco de dados e o retorna."""
        
        try:
            client = Client.find_by_id(value)

            if client:
                return client
            
            client = Client.find_by_rg(value)

            if client:
                return client
            
            client = Client.find_by_cpf(value)
            return client
                    
        except SQLAlchemyError:
            db.rollback()


    @staticmethod
    def mask_client_info(client: Union[Client, dict]) -> dict:
        """Retorna o cliente com suas informações sensíveis mascaradas."""

        client = model_to_dict(client)
        
        client["cpf"] = mask_cpf(client.get("cpf"))
        client["rg"] = mask_rg(client.get("rg"))
        client["phone_number"] = mask_phone_number(client.get("phone_number"))

        return client

    
    @staticmethod
    def update_client(client, field_to_edit, info):
        """Dado o cliente, atualiza algum atributo dele."""

        try:
            setattr(client, field_to_edit, info)
            db.session.commit()

        except SQLAlchemyError:
            db.rollback()


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