from enum import Enum
import re


class RegexPatterns(Enum):
    """
    Class containing common regex patterns used in the code.
    """

    # Only allows: [a-z, A-Z, 0-9, -, _, .]
    USERNAME = re.compile(r"^[a-zA-Z0-9_.-]+$")

    # Only allows: "XX 9XXXXXXXX" or "XX XXXXXXXX"
    PHONE_NUMBER = re.compile(r"^[0-9]{2} 9?[0-9]{8}$")

    # Only allows: "DD/MM/YYYY"
    BIRTH_DATE = re.compile(r"^\d{2}\/\d{2}\/\d{4}$")

    # Only allows: [a-z, A-Z, /, " ", accentuated letters]
    # " " means space
    SANITIZE = re.compile(
        r"[^/\w\s\u00E0-\u00F6\u00F8-\u00FF\u00C0-\u00D6\u00D8-\u00DF]"
    )