from models import Client #type: ignore


def test_client_creation():
    """Tests the method 'Client.create()' from Client's class.
    It should return a 'Client's instance.
    """

    client = Client.create(
        name='Mario',
        rg='987654321',
        cpf='60655920056',
        phone_number='6191118080',
        birth_date='05/05/2025',
    )

    assert isinstance(client, Client)


def test_finding_client_by_id_with_existing_client(clients_objs):
    """Tests the method 'Client.find_by_id()' from Client's class.
    It should return the client associated with that ID.
    """

    for client in clients_objs:
        id = client.id
        query_result = Client.find_by_id(id)

        assert query_result == client


def test_finding_client_by_id_without_existing_client():
    """Tests the method 'Client.find_by_id()' from Client's class.
    It should return 'None'.
    """

    # '10' is a no-existing ID in database
    client = Client.find_by_id(10)
    assert client is None


def test_finding_client_by_cpf_with_existing_client(clients_objs):
    """Tests the method 'Client.find_by_cpf()' from Client's class.
    It should return the client associated with that CPF.
    """

    for client in clients_objs:
        cpf = client.cpf
        query_result = Client.find_by_cpf(cpf)

        assert query_result == client


def test_finding_client_by_cpf_without_existing_client():
    """Tests the method 'Client.find_by_cpf()' from Client's class.
    It should return 'None'.
    """

    # '11111111111' is a no-existing cpf in database
    client = Client.find_by_cpf("11111111111")
    assert client is None


def test_finding_client_by_rg_with_existing_client(clients_objs):
    """Tests the method 'Client.find_by_rg()' from Client's class.
    It should return the client associated with that RG.
    """

    for client in clients_objs:
        rg = client.rg
        query_result = Client.find_by_rg(rg)

        assert client == query_result


def test_finding_client_by_rg_without_existing_client():
    """Tests the method 'Client.find_by_cpf()' from Client's class.
    It should return 'None'.
    """

    # '101020' is a non-existing RG in database
    client = Client.find_by_rg("101020")
    assert client is None


def test_finding_all_clients_with_existing_clients(clients_objs):
    """Tests the method 'Client.find_all()' from Client's class.
    It should return all instances of the 'Client' class.
    """

    all_clients = Client.find_all()

    for client in all_clients:
        assert client in clients_objs


def test_finding_all_clients_without_existing_clients(database):
    """Tests the method 'Client.find_all()' from Client's class.
    It should return an empty list.
    """

    # Clearing all rows from the database
    database.session.query(Client).delete()
    database.session.commit()

    all_clients = Client.find_all()
    assert all_clients == []


def test_counting_clients_with_existing_clients(clients_objs):
    """Tests the method 'Client.count()' from Client's class.
    It should return the total number of rows in the database.
    """

    count = Client.count()
    assert count == len(clients_objs)


def test_counting_clients_without_existing_clients(database):
    """Tests the method 'Client.count()' from Client's class.
    It should return '0'.
    """

    # Clearing all rows from the database
    database.session.query(Client).delete()
    database.session.commit()

    count = Client.count()
    assert count == 0


def test_if_has_any_client_with_existing_clients():
    """Tests the method 'Client.has_any()' from Client's class.
    It should return 'True'
    """

    assert Client.has_any()


def test_if_has_any_client_without_existing_clients(database):
    """Tests the method 'Client.has_any()' from Client's class.
    It should return 'False'
    """

    # Clearing all rows from the database
    database.session.query(Client).delete()
    database.session.commit()

    assert not Client.has_any()