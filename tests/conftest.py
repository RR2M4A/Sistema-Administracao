from datetime import datetime
import pytest
from flask import Flask
from werkzeug.security import generate_password_hash
from models import *
from extensions import db
from utils import BRAZIL_TZ
import validate_docbr
import faker


class AppConfig:
    """Class with Flask's config."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


@pytest.fixture(scope='session', autouse=True)
def app():
    """Returns Flask's WSGI."""

    flask_app = Flask(__name__)
    flask_app.config.from_object(AppConfig)

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()
        yield flask_app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def users_objs():
    """Returns a list of users."""

    return [
        User( # type: ignore
            username='admin_user',
            password_hash=generate_password_hash('123'),
            is_admin=True
        ),

        User( # type: ignore
            username='normal_user',
            password_hash=generate_password_hash('123'),
            is_admin=False
        ),

        User( # type: ignore
            username='inactive_user',
            password_hash=generate_password_hash('123'),
            is_admin=False,
            is_active=False,
        )
    ]


@pytest.fixture
def clients_objs():
    """Returns a list of clients."""

    return [
        Client( # type: ignore
            name='José',
            rg="12345",
            cpf="77596529097",
            phone_number='6110102020',
            birth_date='10/10/2010'
        ),

        Client( # type: ignore
            name='Ronald',
            rg="55555",
            cpf="87879436030",
            phone_number='61993114040',
            birth_date='10/10/2015'

        ),

        Client( # type: ignore
            name='Mary',
            rg="54321",
            cpf="42604392003",
            phone_number='61993113326',
            birth_date='10/11/1978'
        )
    ]


@pytest.fixture
def entrances_objs():
    """Returns a list of entrances."""
    return Entrance.find_all()


@pytest.fixture(scope='session')
def cpf_validator():
    """Returns the 'CPF_Validator' class from 'validate_docbr's lib."""

    return validate_docbr.CPF()


@pytest.fixture(scope='session')
def faker_obj():
    """Returns the 'Faker' class from 'Faker's lib."""

    return faker.Faker("pt_BR")


@pytest.fixture(autouse=True)
def database(users_objs, clients_objs):
    """
    Resets database and inserts fresh test data before each test.
    """

    # Truncate all tables
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())

    # Reinsert users and clients
    db.session.add_all(users_objs)
    db.session.add_all(clients_objs)

    # Add entrances for each client
    entrances = [
        Entrance(entrance=datetime.now(BRAZIL_TZ), client=client)
        for client in clients_objs
    ]

    db.session.add_all(entrances)
    db.session.commit()

    yield db

@pytest.fixture()
def client(app):
    """Returns a client - used for testing routes."""

    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
