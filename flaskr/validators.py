from validate_docbr import CPF
import validate_docbr
from utils import get_days_in_month
from decorators import input_normalized
from datetime import datetime
import re


cpf = CPF()


@input_normalized
def validate_name(input) -> dict:
    """Valida o nome."""

    found_chars = re.search(r"[^a-z\u00E0-\u00F6\u00F8-\u00FF\s]", input)

    if found_chars or not input:
        return {"is_valid": False, "input": "name"}
    
    return {"is_valid": True, "input": "name"}


@input_normalized
def validate_rg(input) -> dict:
    """Valida o rg."""

    if not input:
        return {"is_valid": False, "input": "rg"}

    return {"is_valid": True, "input": "rg"}


@input_normalized
def validate_cpf(input) -> dict:
    """Valida o cpf."""

    is_valid = cpf.validate(input)

    if not is_valid or not input:
        return {"is_valid": False, "input": "cpf"}

    return {"is_valid": True, "input": "cpf"}


@input_normalized
def validate_phone_number(input) -> dict:
    """Valida o número de telefone."""

    is_valid = re.match(r"\([0-9]{2}\) 9?[0-9]{4}-[0-9]{4}", input)

    if not is_valid or not input:
        return {"is_valid": False, "input": "phone-number"}
    
    return {"is_valid": True, "input": "phone-number"}


@input_normalized
def validate_birth_date(input) -> dict:
    """Valida a data de nascimento."""

    is_valid = re.match(r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}$", input)

    if not is_valid or not input:
        return {"is_valid": False, "input": "birth-date"}

    day, month, year = map(int, input.split("/"))
    
    if month < 1 or month > 12:
        return {"is_valid": False, "input": "birth-date"}

    if day < 1 or day > get_days_in_month(month, year):
        return {"is_valid": False, "input": "birth-date"}

    if year > int(datetime.today().year):
        return {"is_valid": False, "input": "birth-date"}
    
    current_date = datetime.today()
    inputed_date = datetime.strptime(input, "%d/%m/%Y")

    if inputed_date > current_date:
        return {"is_valid": False, "input": "birth-date"}

    return {"is_valid": True, "input": "birth-date"}


def validate_all(inputs: dict) -> list[dict]:
    """Valida todos os campos com as funções de validação."""

    name = inputs["name"]
    rg = inputs["rg"]
    cpf = inputs["cpf"]
    phone_number = inputs["phone-number"]
    birth_date = inputs["birth-date"]

    is_valid_name = validate_name(name)
    is_valid_rg = validate_rg(rg)
    is_valid_cpf = validate_cpf(cpf)
    is_valid_phone_number = validate_phone_number(phone_number)
    is_valid_birth_date = validate_birth_date(birth_date)

    return [is_valid_name, is_valid_rg, is_valid_cpf, 
            is_valid_phone_number, is_valid_birth_date]


print(validate_docbr.__file__)