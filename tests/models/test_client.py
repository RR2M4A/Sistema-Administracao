from models import Client #type: ignore


def test_client_creation():

    client = Client.create(
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


def test_finding_client_by_id_with_existing_client():

    client = Client.find_by_id(1)
    assert client is not None
    assert client.name == 'José'
    assert client.rg == '12345'
    assert client.cpf == '77596529097'
    assert client.phone_number == '6110102020'
    assert client.birth_date == '10/10/2010'


def test_finding_client_by_id_without_existing_client():

    client = Client.find_by_id(10)
    assert client is None


def test_finding_client_by_cpf_with_existing_client():

    client = Client.find_by_cpf("77596529097")
    assert client is not None
    assert client.name == 'José'
    assert client.rg == '12345'
    assert client.cpf == '77596529097'
    assert client.phone_number == '6110102020'
    assert client.birth_date == '10/10/2010'


def test_finding_client_by_cpf_without_existing_client():

    client = Client.find_by_cpf("11111111111")
    assert client is None


def test_finding_client_by_rg_with_existing_client():

    client = Client.find_by_rg("12345")
    assert client is not None
    assert client.name == 'José'
    assert client.rg == '12345'
    assert client.cpf == '77596529097'
    assert client.phone_number == '6110102020'
    assert client.birth_date == '10/10/2010'


def test_finding_client_by_rg_without_existing_client():

    client = Client.find_by_rg("101020")
    assert client is None


def test_finding_all_clients_with_existing_clients(clients_objs):

    all_clients = Client.find_all()
    assert all_clients == clients_objs


def test_finding_all_clients_without_existing_clients(database):

    # Limpando todas as linhas da table 'Client' do banco de dados
    database.session.query(Client).delete()
    database.session.commit()

    all_clients = Client.find_all()
    assert all_clients == []


def test_counting_clients_with_existing_clients():

    count = Client.count()
    assert count == 3


def test_counting_clients_without_existing_clients(database):

    # Limpando todas as linhas da table 'Client' do banco de dados
    database.session.query(Client).delete()
    database.session.commit()

    count = Client.count()
    assert count == 0


def test_if_has_any_client_with_existing_clients():

    has_any = Client.has_any()
    assert has_any


def test_if_has_any_client_without_existing_clients(database):

    # Limpando todas as linhas da table 'Client' do banco de dados
    database.session.query(Client).delete()
    database.session.commit()

    has_any = Client.has_any()
    assert not has_any