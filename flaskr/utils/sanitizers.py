from utils.regex import RegexPatterns
import re


def sanitize(value) -> str:
    """Remove caracteres indesejados, preservando letras,
    números e espaços.
    """

    value = str(value).strip().lower()
    pattern = RegexPatterns.SANITIZE.value

    return re.sub(pattern, "", value)



def sanitize_many(d: dict) -> dict[str]:
    """Aplica a sanitização a um dicionário e o retorna."""

    for key, value in d.items():
        d[key] = sanitize(value)

    return d