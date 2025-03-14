from models.client import Client
from models.entrance import Entrance
from extensions.database import db
from sqlalchemy.exc import SQLAlchemyError


class SystemService:


    @staticmethod
    def create_client(data: dict):
        try:
            return Client.create(data)
        except SQLAlchemyError:
            db.rollback()


    @staticmethod
    def find_client(cpf: str):
        try:
            return Client.find_one(cpf)
        except SQLAlchemyError:
            db.rollback()


    @staticmethod
    def create_entrance(client: Client):
        try:
            return Entrance.create(client)
        except SQLAlchemyError:
            db.rollback()
