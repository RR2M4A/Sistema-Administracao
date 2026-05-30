import re


def format_phone_number(value) -> str:
    """
    Formats a phone number to (XX) XXXXX-XXXX or (XX) XXXX-XXXX.
    """

    value = re.sub(r"[^0-9]", "", str(value))

    # SmartPhone (11 digits): (11) 91234-5678
    if len(value) == 11:
        return f"({value[:2]}) {value[2:7]}-{value[7:]}"

    # Phone (10 digits): (11) 1234-5678
    if len(value) == 10:
        return f"({value[:2]}) {value[2:6]}-{value[6:]}"

    # Other
    return value


def format_cpf(value) -> str:
    """
    Formats a cpf (numeric-only at the start) to XXX.XXX.XXX-XX.
    """

    value = re.sub(r"[^0-9]", "", str(value))

    if len(value) == 11:
        return re.sub(r"(\d{3})(\d{3})(\d{3})(\d{2})", r"\1.\2.\3-\4", value)

    return value
