import re


def sanitize(value):
    """Remove caracteres indesejados, preservando letras, 
    números e espaços.
    """

    value = str(value).strip().lower()
    value = re.sub(r"[^\/\w\s\u00E0-\u00F6\u00F8-\u00FF]", "", value)
    return value


def sanitize_many(d: dict):
    """Aplica a sanitização a um dicionário e o retorna."""

    for key, value in d.items():
        d[key] = sanitize(value)

    return d