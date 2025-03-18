from typing import Union, List
from models.client import Client
from models.entrance import Entrance
from extensions.database import db
from sqlalchemy.exc import SQLAlchemyError
from utils.masks import mask_cpf, mask_rg, mask_phone_number


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
    def find_client(*values) -> Client:
        """Busca pelo cliente no banco de dados e o retorna."""
        
        try:
            for value in values:
                client = Client.find_one(value)

                if client:
                    return client
                    
        except SQLAlchemyError:
            db.rollback()


    @staticmethod
    def mask_client_info(client: Union[Client, dict]) -> dict:
        """Retorna o cliente com suas informações sensíveis mascaradas."""
        
        if not isinstance(client, dict):
            client = client.__dict__

        client["cpf"] = mask_cpf(client.get("cpf"))
        client["rg"] = mask_rg(client.get("rg"))
        client["phone_number"] = mask_phone_number(client.get("phone_number"))

        return client


    @classmethod
    def get_masked_clients(cls) -> List[dict]:
        """Retorna todos os clientes armazenados no banco de dados,
        com suas informações já mascaradas.
        """

        try:
            clients = Client.find_all()
            masked_clients = []

            for client in clients:
                client = cls.mask_client_info(client)
                masked_clients.append(client)

            return masked_clients
    
        except SQLAlchemyError:
            db.rollback()