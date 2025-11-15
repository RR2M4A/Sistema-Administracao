from utils import regex
import pytest


@pytest.mark.parametrize('valid_username', [
    "normaluser",
    "NORMAL_USER",
    "-hiphen-USER-",
    "NUMBERED_User123",
    "DOTTED.USER.123",
])
def test_username_regex_valid(valid_username):
    """
    Tests the 'USERNAME' regex from 'regex.py'.
    It should return a non-empty Match object.
    """

    assert regex.RegexPatterns.USERNAME.value.fullmatch(valid_username)


@pytest.mark.parametrize('invalid_username', [
    "user with space",
    "user!@#$%¨&*()/\\|",
    "accentuated_úsér",
    "",
])
def test_username_regex_invalid(invalid_username):
    """
    Tests the 'USERNAME' regex from 'regex.py'.
    It should return 'None' for the listed values.
    """

    assert not regex.RegexPatterns.USERNAME.value.fullmatch(invalid_username)


@pytest.mark.parametrize('valid_phone', [
    "11 987654321",
    "21 87654321"
])
def test_phone_number_regex_valid(valid_phone):
    """
    Tests the 'PHONE_NUMBER' regex from 'regex.py'.
    It should return a non-empty Match object.
    """

    assert regex.RegexPatterns.PHONE_NUMBER.value.fullmatch(valid_phone)


@pytest.mark.parametrize('invalid_phone', [
    "11987654321",
    "1 12345678",
    "11 1234567",
    "11 9123456789"
])
def test_phone_number_regex_invalid(invalid_phone):
    """
    Tests the 'PHONE_NUMBER' regex from 'regex.py'.
    It should return 'None' for the listed values.
    """

    assert not regex.RegexPatterns.PHONE_NUMBER.value.fullmatch(invalid_phone)


@pytest.mark.parametrize('valid_date', [
    "25/12/2025",
    "01/01/1990",
    "31/07/2000"
])
def test_birth_date_regex_valid(valid_date):
    """
    Tests the 'BIRTH_DATE' regex from 'regex.py'.
    It should return 'valid_date' string.
    """

    assert regex.RegexPatterns.BIRTH_DATE.value.fullmatch(valid_date)


@pytest.mark.parametrize('invalid_date', [
    "25-12-2025",
    "25/12/25",
    "2025/12/25",
    "1/1/2000",
    "10-10-2023"
])
def test_birth_date_regex_invalid(invalid_date):
    """
    Tests the 'BIRTH_DATE' regex from 'regex.py'.
    It should return 'None' for the listed values.
    """

    assert not regex.RegexPatterns.BIRTH_DATE.value.fullmatch(invalid_date)


def test_sanitize_regex():
    """
    Tests the 'SANITIZE' regex from 'regex.py'.
    It should correctly remove invalid characters from a string.
    """

    dirty_string = "Usuário_123!@# (teste) com acentuação/barra"
    expected_clean_string = "Usuário_123 teste com acentuação/barra"

    res = regex.RegexPatterns.SANITIZE.value.sub("", dirty_string)

    assert res == expected_clean_string