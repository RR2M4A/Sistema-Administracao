from utils import date_utils
from datetime import datetime
import pytest


def test_to_start_of_day_with_valid_string():
    """
    Tests the 'to_start_of_day()' method from 'date_utils.py'.
    It should return a valid datetime object.
    """

    expected = datetime(2025, 10, 10, 0, 0, 0, 0)
    result = date_utils.to_start_of_day("10/10/2025")

    assert result == expected


@pytest.mark.parametrize('invalid_value', [
    '10.10.2010', '10\\10\\2010',
    'october-10th', '21-11-2005',
    '00/00/0000'
])
def test_to_start_of_day_with_invalid_string(invalid_value):
    """
    Tests the 'to_start_of_day()' method from 'date_utils.py'.
    It should return a 'ValueError'.
    """

    with pytest.raises(ValueError):
        date_utils.to_start_of_day(invalid_value)


def test_to_end_of_day_with_valid_string():
    """
    Tests the 'to_end_of_day()' method from 'date_utils.py'.
    It should return a valid datetime object.
    """

    expected = datetime(2025, 10, 10, 23, 59, 59, 999999)
    result = date_utils.to_end_of_day("10/10/2025")

    assert result == expected


@pytest.mark.parametrize('invalid_value', [
    '10.10.2010', '10\\10\\2010',
    'october-10th', '21-11-2005',
    '00/00/0000'
])
def test_to_end_of_day_with_invalid_string(invalid_value):
    """
    Tests the 'to_end_of_day()' method from 'date_utils.py'.
    It should return a 'ValueError'.
    """

    with pytest.raises(ValueError):
        date_utils.to_end_of_day(invalid_value)