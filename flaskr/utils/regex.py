from enum import Enum
import re


class RegexPatterns(Enum):

    USERNAME = re.compile(r"^[\w.-]+$")

    PHONE_NUMBER = re.compile(r"[0-9]{2} 9?[0-9]{4}[0-9]{4}")

    BIRTH_DATE = re.compile(
        r"(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/(19[0-9]{2}|20[0-9]{2})"
    )

    SANITIZE = re.compile(
        r"[^\/\w\s\u00E0-\u00F6\u00F8-\u00FF]"
    )