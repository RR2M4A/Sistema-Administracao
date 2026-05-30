import pytest
from ..utils.formatters import format_phone_number, format_cpf
from ..utils.regex_patterns import RegexPatterns

class TestFormatters:
    """
    Class responsible for holding tests regarding
    the 'formatters.py' file.
    """

    @pytest.mark.parametrize("input_val, expected", [
        ("61999998888", "(61) 99999-8888"),
        ("6133332222", "(61) 3333-2222"),
        ("61 99999 8888", "(61) 99999-8888"),
        ("(61)999998888", "(61) 99999-8888"),
        ("123abc45678901", "(12) 34567-8901"),
        ("123", "123"),
        ("", ""),
    ])
    def test_format_phone_number(self, input_val, expected):
        assert format_phone_number(input_val) == expected


    @pytest.mark.parametrize("input_val, expected", [
        ("12345678901", "123.456.789-01"),
        ("123.456.789-01", "123.456.789-01"),
        ("123 456 789 01", "123.456.789-01"),
        ("123abc45678901", "123.456.789-01"),
        ("123456", "123456"),
        (12345678901, "123.456.789-01"),
    ])
    def test_format_cpf(self, input_val, expected):
        assert format_cpf(input_val) == expected


class TestRegexPatterns:
    """
    Class responsible for holding tests regarding to the
    'regex_patterns.py' file.
    """

    @pytest.mark.parametrize("phone, expected", [
        ("61 988887777", True),
        ("61 33332222", True),
        ("61988887777", False),
        ("61 88887777", True),
        ("6 988887777", False),
        ("61 98888777", True),
        ("AA 988887777", False),
    ])
    def test_phone_number_regex(self, phone, expected):
        assert bool(RegexPatterns.PHONE_NUMBER.value.fullmatch(phone)) == expected


    @pytest.mark.parametrize("date, expected", [
        ("01/01/1990", True),
        ("31/12/2023", True),
        ("1/1/1990", False),
        ("01-01-1990", False),
        ("01/01/90", False),
        ("AA/BB/CCCC", False),
    ])
    def test_birth_date_regex(self, date, expected):
        assert bool(RegexPatterns.BIRTH_DATE.value.fullmatch(date)) == expected


    @pytest.mark.parametrize("username, expected", [
        ("jose.silva", True),
        ("user_123", True),
        ("user-name", True),
        ("jose silva", False),
        ("jose@123", False),
    ])
    def test_username_regex(self, username, expected):
        assert bool(RegexPatterns.USERNAME.value.fullmatch(username)) == expected