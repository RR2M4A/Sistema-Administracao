from models import Entrance #type: ignore


def test_entrance_creation(clients_objs):
    """Testa o método 'Entrance.create()' da classe 'Entrance'.
    É válido se 'Entrance.create()' retorna uma instância de 'Entrance'.
    """

    entrance = Entrance.create(clients_objs[0])

    assert entrance is not None
    assert entrance.client == clients_objs[0]


def test_finding_all_entrances_with_existing_entrances(entrances_objs):
    """Testa o método 'Entrance.find_all()' da classe 'Entrance'.
    É válido se 'Entrance.find_all()' retorna as instâncias da fixture.
    """

    all_entrances = Entrance.find_all()

    # Garantindo que as entradas estejam em ordem decrescente
    expected_order = entrances_objs[::-1]

    assert all_entrances is not None
    assert all_entrances == expected_order


def test_finding_all_entrances_without_existing_entrances(database):
    """Testa o método 'Entrance.find_all()' da classe 'Entrance'.
    É válido se 'Entrance.find_all()' retornar uma lista vazia.
    """

    # Limpando todas as linhas da table 'Entrance' do banco de dados
    database.session.query(Entrance).delete()
    database.session.commit()

    all_entrances = Entrance.find_all()
    assert all_entrances == []


def test_counting_entrances_with_existing_entrances(entrances_objs):
    """Testa o método 'Entrance.count()' da classe 'Entrance'.
    É válido se 'Entrance.count()' retornar o tamanho da fixture 'entrance_objs'.
    """

    count = Entrance.count()
    assert count == len(entrances_objs)


def test_counting_entrances_without_existing_entrances(database):
    """Testa o método 'Entrance.count()' da classe 'Entrance'.
    É válido se 'Entrance.count()' retornar o inteiro 0.
    """

    # Limpando todas as linhas da table 'Entrance' do banco de dados
    database.session.query(Entrance).delete()
    database.session.commit()

    count = Entrance.count()
    assert count == 0
