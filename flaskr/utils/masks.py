def mask_cpf(cpf: str):
    """Retorna o cpf mascarado."""
    
    return "{}.***.***-{}".format(cpf[:3], cpf[-2:])


def mask_rg(rg: str):
    """Retorna o rg mascarado.
    
    Como o RG tem diversos padrões a depender do estado, a fim de segurança
    e praticidade, o padrão será de 7 asteriscos ('*').
    """

    return "*" * 7


def mask_phone_number(phone_number: str):
    """Retorna o número de telefone mascarado."""

    if len(phone_number) == 12:
        return "{} *****-{}".format(phone_number[:2], phone_number[-4:])
    return "{} ****-{}".format(phone_number[:2], phone_number[-4:])