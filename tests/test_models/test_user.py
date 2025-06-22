from models import User #type: ignore
from werkzeug.security import generate_password_hash, check_password_hash


def test_user_creation():

    user = User.create(
        username = 'user',
        password_hash = generate_password_hash('123'),
        is_admin = False
    )

    assert isinstance(user, User)
    assert user.username == 'user'
    assert check_password_hash(user.password_hash, '123')
    assert not user.is_admin


def test_finding_user_by_username_with_existing_user():

    user = User.find_by_username('admin_user')

    assert user is not None
    assert user.username == 'admin_user'
    assert check_password_hash(user.password_hash, '123')
    assert user.is_admin


def test_finding_user_by_username_without_existing_user():

    user = User.find_by_username('admin_user_2')
    assert user is None


def test_finding_user_by_id_with_existing_user():

    user = User.find_by_id(1)

    assert user is not None
    assert user.username == 'admin_user'
    assert check_password_hash(user.password_hash, '123')
    assert user.is_admin


def test_finding_user_by_id_without_existing_user():

    user = User.find_by_id(10)
    assert user is None


def test_finding_all_users_with_existing_users(users_objs):

    all_users = User.find_all()
    assert all_users == users_objs


def test_finding_all_users_without_existing_users(database):

    # Limpando todas as linhas da table 'User' do banco de dados
    database.session.query(User).delete()
    database.session.commit()

    all_users = User.find_all()
    assert all_users == []


def test_if_has_any_user_with_existing_users():

    has_any = User.has_any()
    assert has_any


def test_if_has_any_user_without_existing_users(database):

    # Limpando todas as linhas da table 'User' do banco de dados
    database.session.query(User).delete()
    database.session.commit()

    has_any = User.has_any()
    assert not has_any


def test_checking_password_with_valid_password():

    user = User.find_by_id(1)

    assert user is not None
    assert user.check_password('123')


def test_checking_password_with_invalid_password():

    user = User.find_by_id(1)

    assert user is not None
    assert not user.check_password('321')