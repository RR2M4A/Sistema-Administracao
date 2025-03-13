from models.client import Client
from models.entrance import Entrance
from validation_service import ValidationService

class SystemService:

    @staticmethod
    def find_or_create_client(data: dict):
        

        ValidationService.validate_all(data)
        client = Client.find(data.get("cpf")).scalar_one_or_none()

        if client:
            Entrance.create(client)
            is_new = False
            operation = "updated"
        else:
            client = Client.create(data)
            Entrance.create(client)
            is_new = True
            operation = "created"

        return is_new, operation
