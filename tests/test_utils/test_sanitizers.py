from utils import sanitizers
import pytest


@pytest.mark.parametrize("inputed, expected", [
    ("Úser_123!@#", "Úser_123"),
    ("  text with spaces  ", "text with spaces"),
    ("with válíd áccénts", "with válíd áccénts"),
    ("with/bar", "with/bar"),
    ("with-hiphen", "withhiphen"),
    ("Word! With? Symbols!", "Word With Symbols"),
    ("", ""),
    (12345, "12345"),
    (None, "None"),
])
def test_sanitize(inputed, expected):
    """
    Tests the 'sanitize()' method from 'sanitizers.py'.
    It should return the inputed string, cleaned.
    """

    assert sanitizers.sanitize(inputed) == expected


def test_sanitize_many():
    """
    Tests the 'sanitize_many()' method from 'sanitizers.py'.
    It should sanitize all values of a dictionary, returning a copy.
    """

    data = {
        "name": "User!@#",
        "city": "Brasília??",
        "note": "text/with/bar",
    }

    expected = {
        "name": "User",
        "city": "Brasília",
        "note": "text/with/bar"
    }

    assert sanitizers.sanitize_many(data) == expected

