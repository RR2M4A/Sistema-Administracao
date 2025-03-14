from validate_docbr import CPF
from utils.date_utils import get_days_in_month
from utils.decorators import input_normalized
from datetime import datetime
import re


class ValidationService:

    def __init__(self):
        self.cpf_validator = CPF()

        self.VALIDATORS = {
            "name": self.validate_name,
            "rg": self.validate_rg,
            "cpf": self.validate_cpf,
            "phone-number": self.validate_phone_number,
            "birth-date": self.validate_birth_date
        }


    @input_normalized
    def validate_name(self, input) -> dict:
        """Valida o nome."""

        found_chars = re.search(r"[^a-z\u00E0-\u00F6\u00F8-\u00FF\s]", input, re.UNICODE)

        if found_chars or not input:
            return (False, "Nome inválido.")
        
        return (True, "")


    @input_normalized
    def validate_rg(self, input) -> dict:
        """Valida o rg."""

        if not input:
            return (False, "Rg inválido.")

        return (True, "")


    @input_normalized
    def validate_cpf(self, input) -> dict:
        """Valida o cpf."""

        is_valid = self.cpf_validator.validate(input)

        if not is_valid or not input:
            return (False, "CPF inválido.")

        return (True, "")


    @input_normalized
    def validate_phone_number(self, input) -> dict:
        """Valida o número de telefone."""

        is_valid = re.match(r"\([0-9]{2}\) 9?[0-9]{4}-[0-9]{4}", input)

        if not is_valid or not input:
            return (False, "Telefone inválido.")
        
        return (True, "")


    @input_normalized
    def validate_birth_date(self, input) -> dict:
        """Valida a data de nascimento."""

        is_valid = re.match(r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}$", input)

        if not is_valid or not input:
            return (False, "Data de nascimento inválida.")

        day, month, year = map(int, input.split("/"))
        
        if month < 1 or month > 12:
            return (False, "Data de nascimento inválida.")

        if day < 1 or day > get_days_in_month(month, year):
            return (False, "Data de nascimento inválida.")

        if year > int(datetime.today().year):
            return (False, "Data de nascimento inválida.")
        
        current_date = datetime.today()
        inputed_date = datetime.strptime(input, "%d/%m/%Y")

        if inputed_date > current_date:
            return (False, "Data de nascimento inválida.")

        return (True, "")


    def validate_all(self, inputs: dict) -> list[dict]:
        """Valida todos os campos com as funções de validação."""

        validation_result = {}

        for key, value in self.VALIDATORS.items():
            is_valid, msg = value(inputs.get(key))

            if not is_valid:
                validation_result[key] = msg

        return validation_result