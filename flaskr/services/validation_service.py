from typing import List
from validate_docbr import CPF
from utils.date_utils import get_days_in_month
from utils.decorators import input_normalized
from datetime import datetime
import re


class ValidationService:

    CPF_VALIDATOR = CPF()

    VALIDATORS = {
        "name": "validate_name",
        "rg": "validate_rg",
        "cpf": "validate_cpf",
        "phone-number": "validate_phone_number",
        "birth-date": "validate_birth_date"
    }


    @classmethod
    @input_normalized
    def validate_name(cls, input: str) -> tuple:
        """Valida o nome."""

        found_chars = re.search(r"[^a-z\u00E0-\u00F6\u00F8-\u00FF\s]", input, re.UNICODE)

        if found_chars or not input:
            return ("name", False)
        
        return ("name", True)


    @classmethod
    @input_normalized
    def validate_rg(cls, input: str) -> tuple:
        """Valida o rg."""

        if not input:
            return ("rg", False)

        return ("rg", True)


    @classmethod
    @input_normalized
    def validate_cpf(cls, input: str) -> tuple:
        """Valida o cpf."""

        is_valid = cls.CPF_VALIDATOR.validate(input)

        if not is_valid or not input:
            return ("cpf", False)

        return ("cpf", True)


    @classmethod
    @input_normalized
    def validate_phone_number(cls, input: str) -> tuple:
        """Valida o número de telefone."""

        is_valid = re.match(r"\([0-9]{2}\) 9?[0-9]{4}-[0-9]{4}", input)

        if not is_valid or not input:
            return ("phone-number", False)
        
        return ("phone-number", True)


    @classmethod
    @input_normalized
    def validate_birth_date(cls, input: str) -> tuple:
        """Valida a data de nascimento."""

        is_valid = re.match(r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}$", input)

        if not is_valid or not input:
            return ("birth-date", False)

        day, month, year = map(int, input.split("/"))
        
        if month < 1 or month > 12:
            return ("birth-date", False)

        if day < 1 or day > get_days_in_month(month, year):
            return ("birth-date", False)

        if year > int(datetime.today().year):
            return ("birth-date", False)
        
        current_date = datetime.today()
        inputed_date = datetime.strptime(input, "%d/%m/%Y")

        if inputed_date > current_date:
            return ("birth-date", False)

        return ("birth-date", True)


    @classmethod
    def validate_all(cls, inputs: dict) -> list:
        """Valida todos os campos com as funções de validação."""

        errors = []

        for key, value in cls.VALIDATORS.items():
            function = getattr(cls, value)

            input_name, is_valid = function(inputs.get(key))

            if not is_valid:
                errors.append(input_name)

        return errors