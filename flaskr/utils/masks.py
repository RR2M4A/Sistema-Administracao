from typing import Optional
from models import Client
from utils.converters import model_to_dict


def mask_cpf(cpf: Optional[str]) -> str:
    """Returns the masked CPF."""

    if not cpf:
        return "***.***.***-**"

    return f"{cpf[:3]}.***.***-{cpf[-2:]}"


def mask_rg(rg: Optional[str]) -> str:
    """
    Returns the masked RG.
    Since RG has different patterns depending on the state,
    for security and simplicity, the pattern will be 7 asterisks.
    """

    return "*" * 7


def mask_phone_number(phone_number: str) -> str:
    """Returns the masked phone number."""

    if not phone_number:
        return ""

    if len(phone_number) == 12:
        return "({}) *****-{}".format(phone_number[:2], phone_number[-4:])
    return "({}) ****-{}".format(phone_number[:2], phone_number[-4:])


def mask_client_info(client: 'Client') -> dict:
    """Returns a dict of client info with sensitive data masked."""

    client = model_to_dict(client)

    client["cpf"] = mask_cpf(client.get("cpf"))
    client["rg"] = mask_rg(client.get("rg"))
    client["phone_number"] = mask_phone_number(client.get("phone_number"))

    return client
