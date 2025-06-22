from datetime import datetime
import pytest
from flask import Flask
from werkzeug.security import generate_password_hash
from models import *
from extensions import db # type: ignore
from utils import BRAZIL_TZ # type: ignore


class AppConfig:
    """Classe com as configurações do app flask."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


@pytest.fixture(scope='session', autouse=True)
def app():
    """Fixture que cria e retorna o Flask WSGI."""

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
    """Fixture que retorna uma lista de usuários fictícios."""

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
    """Fixture que retorna uma lista de clientes fictícios."""

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
def entrances_objs(clients_objs):
    """Fixture que retorna uma lista de entradas fictícias."""

    return [
        Entrance(entrance=datetime.now(BRAZIL_TZ), client=clients_objs[0]), # type: ignore
        Entrance(entrance=datetime.now(BRAZIL_TZ), client=clients_objs[1]), # type: ignore
        Entrance(entrance=datetime.now(BRAZIL_TZ), client=clients_objs[2]), # type: ignore
    ]


@pytest.fixture(autouse=True)
def database(users_objs, clients_objs, entrances_objs):
    """Fixture que retorna uma instância do banco de dados, alimentado
    pelos dados fictícios.
    """

    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

    db.session.add_all(users_objs)
    db.session.add_all(clients_objs)
    db.session.add_all(entrances_objs)
    db.session.commit()

    yield db


@pytest.fixture()
def client(app):
    """Fixture que retorna o cliente - agente para as requisições nas rotas."""

    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
