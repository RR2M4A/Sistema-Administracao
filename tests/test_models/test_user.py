from models import User #type: ignore
from werkzeug.security import generate_password_hash, check_password_hash


def test_user_creation():
    """Testa o método 'User.create()' da classe 'User'.
    É válido se 'User.create()' retorna uma instância de 'User'.
    """

    user = User.create(
        username = 'user',
        password_hash = generate_password_hash('123'),
        is_admin = False
    )

    assert isinstance(user, User)
    assert user.username == 'user'
    assert check_password_hash(user.password_hash, '123')
    assert not user.is_admin


def test_finding_user_by_username_with_existing_user(users_objs):
    """Testa o método 'User.find_by_username()' da classe 'User'.
    É válido se 'User.find_by_username()' retornar a instância da fixture.
    """

    user = User.find_by_username('admin_user')
    assert user in users_objs


def test_finding_user_by_username_without_existing_user():
    """Testa o método 'User.find_by_username()' da classe 'User'.
    É válido se 'User.find_by_username()' retornar 'None'.
    """

    user = User.find_by_username('admin_user_2')
    assert user is None


def test_finding_user_by_id_with_existing_user(users_objs):
    """Testa o método 'User.find_by_id()' da classe 'User'.
    É válido se 'User.find_by_id()' retornar a instância da fixture.
    """

    user = User.find_by_id(1)
    assert user in users_objs


def test_finding_user_by_id_without_existing_user():
    """Testa o método 'User.find_by_id()' da classe 'User'.
    É válido se 'User.find_by_id()' retornar 'None'.
    """

    user = User.find_by_id(10)
    assert user is None


def test_finding_all_users_with_existing_users(users_objs):
    """Testa o método 'User.find_all()' da classe 'User'.
    É válido se 'User.find_all()' retornar as instâncias da fixture na mesma ordem.
    """

    all_users = User.find_all()
    assert all_users == users_objs


def test_finding_all_users_without_existing_users(database):
    """Testa o método 'User.find_all()' da classe 'User'.
    É válido se 'User.find_all()' retornar uma lista vazia.
    """

    # Limpando todas as linhas da table 'User' do banco de dados
    database.session.query(User).delete()
    database.session.commit()

    all_users = User.find_all()
    assert all_users == []


def test_if_has_any_user_with_existing_users():
    """Testa o método 'User.has_any()' da classe 'User'.
    É válido se 'User.has_any()' retornar 'True'.
    """

    has_any = User.has_any()
    assert has_any


def test_if_has_any_user_without_existing_users(database):
    """Testa o método 'User.has_any()' da classe 'User'.
    É válido se 'User.has_any()' retornar 'False'.
    """

    # Limpando todas as linhas da table 'User' do banco de dados
    database.session.query(User).delete()
    database.session.commit()

    has_any = User.has_any()
    assert not has_any


def test_checking_password_with_valid_password():
    """Testa o método 'User.check_password()' da classe 'User'.
    É válido se 'User.check_password()' retornar 'True'.
    """

    user = User.find_by_id(1)

    assert user is not None
    assert user.check_password('123')


def test_checking_password_with_invalid_password():
    """Testa o método 'User.check_pasword()' da classe 'User'.
    É válido se 'User.check_pasword()' retornar 'False'.
    """

    user = User.find_by_id(1)

    assert user is not None
    assert not user.check_password('321')