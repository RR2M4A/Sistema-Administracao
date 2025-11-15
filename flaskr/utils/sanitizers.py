from utils.regex import RegexPatterns
import re
from typing import Dict, Any


def sanitize(value) -> str:
    """
    Removes unwanted characters, preserving letters,
    numbers, and spaces, and strips whitespace.
    """

    value = str(value).strip()
    pattern = RegexPatterns.SANITIZE.value

    return re.sub(pattern, "", value)


def sanitize_many(data: dict) -> Dict[str, Any]:
    """
    Applies sanitization to all values in a dictionary
    and returns a new, sanitized dictionary.
    """

    return {key: sanitize(value) for key, value in data.items()}