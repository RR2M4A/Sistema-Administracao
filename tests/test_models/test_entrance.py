from models import Entrance #type: ignore


def test_entrance_creation(clients_objs):
    """Tests the method 'Entrance.create()' from Entrance's class.
    It should return a 'Entrance's instance.
    """

    entrance = Entrance.create(client=clients_objs[0])

    assert isinstance(entrance, Entrance)
    assert entrance.client == clients_objs[0]


def test_finding_entrances_by_client_with_existing_client(entrances_objs):
    """Tests the method 'Entrance.find_by_client()' from Entrance's class.
    It should return an array of a client's entrances.
    """

    array = Entrance.find_by_client(entrances_objs[0].id)
    assert len(array) > 0


def test_finding_entrances_by_client_without_existing_client():
    """Tests the method 'Entrance.find_by_client()' from Entrance's class.
    It should return an empty list.
    """

    # '1000' is a non-existing client id
    array = Entrance.find_by_client(1000)
    assert array == []


def test_finding_all_entrances_with_existing_entrances(entrances_objs):
    """Tests the method 'Entrance.find_all()' from Entrance's class.
    Is thould return all Entrance's instances of the database.
    """

    for entrance in entrances_objs:
        assert isinstance(entrance, Entrance)


def test_finding_all_entrances_without_existing_entrances(database):
    """Tests the method 'Entrance.find_all()' from Entrance's class.
    It should return an empty list.
    """

    # Limpando todas as linhas da table 'Entrance' do banco de dados
    database.session.query(Entrance).delete()
    database.session.commit()

    all_entrances = Entrance.find_all()
    assert all_entrances == []


def test_counting_entrances_with_existing_entrances(entrances_objs):
    """Tests the method 'Entrance.count()' from Entrance's class.
    It should return the total number of rows in the database.
    """

    count = Entrance.count()
    assert count == len(entrances_objs)


def test_counting_entrances_without_existing_entrances(database):
    """Tests the method 'Entrance.count()' from Entrance's class.
    It should return '0'.
    """

    # Limpando todas as linhas da table 'Entrance' do banco de dados
    database.session.query(Entrance).delete()
    database.session.commit()

    count = Entrance.count()
    assert count == 0
