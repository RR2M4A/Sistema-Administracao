from utils import converters
import pytest


UNWANTED_ATTRIBUTES = ["password_hash"]


def test_model_to_dict_with_a_valid_SQLAlchemy_obj(users_objs):
    """
    Tests the 'model_to_dict()' method from 'converters.py'.
    It should return a dict with the targeted attributes removed.
    """

    for user in users_objs:

        clean_user = converters.model_to_dict(user)

        for attribute in UNWANTED_ATTRIBUTES:
            assert attribute not in clean_user


def test_model_to_dict_returns_a_copy_not_reference(users_objs):
    """
    Tests the 'model_to_dict()' method from 'converters.py'.
    It should return the copy of the dict, not its reference.
    """

    for client in users_objs:
        clean_client = converters.model_to_dict(client)

        assert clean_client is not client.__dict__


@pytest.mark.parametrize('obj', [
    {}, [], (),
    [10, 20, 30], (10, 20, 30),
    "random_string", 999,
])
def test_model_to_dict_with_invalid_obj(obj):
    """
    Tests the 'model_to_dict()' method from 'converters.py'.
    It should return an empty dict.
    """

    cleaned_obj = converters.model_to_dict(obj)
    assert cleaned_obj == {}



