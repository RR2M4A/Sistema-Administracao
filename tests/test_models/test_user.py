from models import User #type: ignore
from werkzeug.security import generate_password_hash, check_password_hash


def test_user_creation():
    """Tests the method 'User.create()' from User's class.
    It should return the 'User's instance.
    """

    user = User.create(
        username = 'user',
        password_hash = generate_password_hash('123'),
        is_admin = False
    )

    assert isinstance(user, User)


def test_finding_user_by_username_with_existing_user(users_objs):
    """Tests the method 'User.find_by_username()' from User's class.
    It should return the 'User's instance.
    """

    user = User.find_by_username('admin_user')
    assert user in users_objs


def test_finding_user_by_username_without_existing_user():
    """Tests the method 'User.find_by_username()' from User's class.
    It should return 'None'.
    """

    user = User.find_by_username('admin_user_2')
    assert user is None


def test_finding_user_by_id_with_existing_user(users_objs):
    """Tests the method 'User.find_by_id()' from User's class.
    It should return the 'User's instance.
    """

    user = User.find_by_id(users_objs[0].id)
    assert isinstance(user, User)


def test_finding_user_by_id_without_existing_user():
    """Tests the method 'User.find_by_id()' from User's class.
    It should return 'None'.
    """

    # '10' is a non-existing user id in the fixture
    user = User.find_by_id(10)
    assert user is None


def test_finding_all_users_with_existing_users(users_objs):
    """Tests the method 'User.find_all()' from User's class.
    It should return all instances of 'User' class.
    """

    all_users = User.find_all()
    for user in all_users:
        assert user in users_objs


def test_finding_all_users_without_existing_users(database):
    """Tests the method 'User.find_all()' from User's class.
    It should return an empty list.
    """

    # Clearing all rows from the database
    database.session.query(User).delete()
    database.session.commit()

    all_users = User.find_all()
    assert all_users == []


def test_if_has_any_user_with_existing_users():
    """Tests the method 'User.has_any()' from User's class.
    It should return 'True'.
    """

    has_any = User.has_any()
    assert has_any


def test_if_has_any_user_without_existing_users(database):
    """Tests the method 'User.has_any()' from User's class.
    It should return 'False'.
    """

    # Clearing all rows from the database
    database.session.query(User).delete()
    database.session.commit()

    has_any = User.has_any()
    assert not has_any


def test_checking_password_with_valid_password():
    """Tests the method 'User.check_password()' from User's class.
    It should return 'True'.
    """
    user = User.find_by_id(1)

    assert user is not None
    assert user.check_password('123')


def test_checking_password_with_invalid_password():
    """Tests the method 'User.check_password()' from User's class.
    It should return 'False'.
    """

    user = User.find_by_id(1)

    assert user is not None
    assert not user.check_password('321')