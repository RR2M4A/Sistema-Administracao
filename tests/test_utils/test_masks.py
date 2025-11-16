import pytest
from utils import masks

@pytest.mark.parametrize("cpf, expected", [
    ("12345678901", "123.***.***-01"),
    ("98765432100", "987.***.***-00"),
    (None, "***.***.***-**"),
    ("", "***.***.***-**"),
])
def test_mask_cpf(cpf, expected):
    """
    Tests the method 'mask_cpf()' from 'masks.py' module.
    It should only keep the first three digits and 2 last digits.
    """
    assert masks.mask_cpf(cpf) == expected


def test_mask_rg():
    """
    Tests the method 'mask_rg()' from 'masks.py' module.
    It should always return '*******'.
    """

    assert masks.mask_rg("1234567") == "*******"
    assert masks.mask_rg(None) == "*******"
    assert masks.mask_rg("") == "*******"


@pytest.mark.parametrize("phone, expected", [
    ("", ""),
    (None, ""),
    ("11987654321", "(11) ****-4321"),
    ("119876543210", "(11) *****-3210"),
])
def test_mask_phone_number(phone, expected):
    """
    Tests the method 'mask_phone_number()' from 'masks.py' module.
    It should mask the number.
    """

    assert masks.mask_phone_number(phone) == expected


def test_mask_client_info(clients_objs):
    """
    Tests masking for a list of Client objects.
    Ensures sensitive fields are masked and others preserved.
    """

    for client in clients_objs:
        masked = masks.mask_client_info(client)

        # Masked data
        assert masked["cpf"] == f"{client.cpf[:3]}.***.***-{client.cpf[-2:]}"
        assert masked["rg"] == "*******"
        assert masked["name"] == client.name
        assert masked["birth_date"] == client.birth_date

        original_phone = client.phone_number

        if len(original_phone) == 12:
            "({}) *****-{}".format(original_phone[:2], original_phone[-4:])
        else:
            expected_phone = "({}) ****-{}".format(original_phone[:2], original_phone[-4:])

        assert masked["phone_number"] == expected_phone
