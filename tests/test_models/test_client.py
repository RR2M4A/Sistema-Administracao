from models import Client #type: ignore


def test_client_creation():
    """Testa o método 'Client.create()' da classe 'Client'.
    É válido se 'Client.create()' retorna uma instância de 'Client'.
    """

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


def test_finding_client_by_id_with_existing_client(clients_objs):
    """Testa o método 'Client.find_by_id()' da classe 'Client'.
    É válido se 'Client.find_by_id()' retorna uma instância de 'Client'.
    """

    client = Client.find_by_id(1)
    assert client in clients_objs


def test_finding_client_by_id_without_existing_client():
    """Testa o método 'Client.find_by_id()' da classe 'Client'.
    É válido se 'Client.find_by_id()' retornar 'None'.
    """

    client = Client.find_by_id(10)
    assert client is None


def test_finding_client_by_cpf_with_existing_client(clients_objs):
    """Testa o método 'Client.find_by_cpf()' da classe 'Client'.
    É válido se 'Client.find_by_cpf()' retornar a instância da fixture.
    """

    client = Client.find_by_cpf("77596529097")
    assert client in clients_objs


def test_finding_client_by_cpf_without_existing_client():
    """Testa o método 'Client.find_by_cpf()' da classe 'Client'.
    É válido se 'Client.find_by_cpf()' retornar 'None'.
    """

    client = Client.find_by_cpf("11111111111")
    assert client is None


def test_finding_client_by_rg_with_existing_client(clients_objs):
    """Testa o método 'Client.find_by_rg()' da classe 'Client'.
    É válido se 'Client.find_by_rg()' retornar a instância da fixture.
    """

    client = Client.find_by_rg("12345")
    assert client in clients_objs


def test_finding_client_by_rg_without_existing_client():
    """Testa o método 'Client.find_by_rg()' da classe 'Client'.
    É válido se 'Client.find_by_rg()' retornar 'None'.
    """

    client = Client.find_by_rg("101020")
    assert client is None


def test_finding_all_clients_with_existing_clients(clients_objs):
    """Testa o método 'Client.find_all()' da classe 'Client'.
    É válido se 'Client.find_all()' retornar as instâncias da fixture na mesma ordem.
    """

    all_clients = Client.find_all()
    assert all_clients == clients_objs


def test_finding_all_clients_without_existing_clients(database):
    """Testa o método 'Client.find_all()' da classe 'Client'.
    É válido se 'Client.find_all()' retornar uma lista vazia.
    """

    # Limpando todas as linhas da table 'Client' do banco de dados
    database.session.query(Client).delete()
    database.session.commit()

    all_clients = Client.find_all()
    assert all_clients == []


def test_counting_clients_with_existing_clients(clients_objs):
    """Testa o método 'Client.count()' da classe 'Client'.
    É válido se 'Client.count()' retornar o tamanho da fixture 'clients_objs'.
    """

    count = Client.count()
    assert count == len(clients_objs)


def test_counting_clients_without_existing_clients(database):
    """Testa o método 'Client.count()' da classe 'Client'.
    É válido se 'Client.count()' retornar o inteiro 0.
    """

    # Limpando todas as linhas da table 'Client' do banco de dados
    database.session.query(Client).delete()
    database.session.commit()

    count = Client.count()
    assert count == 0


def test_if_has_any_client_with_existing_clients():
    """Testa o método 'Client.has_any()' da classe 'Client'.
    É válido se 'Client.has_any()' retornar 'True'.
    """

    has_any = Client.has_any()
    assert has_any


def test_if_has_any_client_without_existing_clients(database):
    """Testa o método 'Client.has_any()' da classe 'Client'.
    É válido se 'Client.has_any()' retornar 'False'.
    """

    # Limpando todas as linhas da table 'Client' do banco de dados
    database.session.query(Client).delete()
    database.session.commit()

    has_any = Client.has_any()
    assert not has_any