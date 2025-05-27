from enum import Enum
import re


class RegexPatterns(Enum):

    USERNAME = re.compile(r"^[\w.-]+$")