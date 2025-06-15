from models import Client #type: ignore


def test_client_creation():

    client = Client(
        name='Mario',
        rg='987654321',
        cpf='60655920056',
        phone_number='6191118080',
        birth_date='05/05/2025',
    )

    assert isinstance(client, Client)
    assert client.name == 'Mario'
    assert client.rg == '987654321'
    assert client.cpf == '60655920056'
    assert client.phone_number == '6191118080'
    assert client.birth_date == '05/05/2025'