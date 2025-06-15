import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash as gph
from models import *


test_db = SQLAlchemy()

class AppConfig:
    """Classe com as configurações do app flask."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


@pytest.fixture(scope='session')
def app():
    """Fixture que cria e retorna o Flask WSGI."""

    flask_app = Flask(__name__)
    flask_app.config.from_object(AppConfig)

    test_db.init_app(flask_app)

    with flask_app.app_context():
        test_db.create_all()
        yield flask_app

        test_db.session.remove()
        test_db.drop_all()


@pytest.fixture()
def users():
    return [
        User(username='admin_user', password=gph('123'), is_admin=True), # type: ignore
        User(username='normal_user', password=gph('123'), is_admin=False), # type: ignore
        User(username='inactive_user', password=gph('123'), is_admin=False, is_active=False), # type: ignore
    ]


@pytest.fixture()
def clients():
    return [
        Client(name='José', rg="12345", cpf="77596529097", # type: ignore
               phone_number='6110102020', birth_date='10/10/2010'),
        Client(name='Ronald', rg="55555", cpf="87879436030", # type: ignore
               phone_number='61993114040', birth_date='10/10/2015'),
        Client(name='Mary', rg="54321", cpf="42604392003", # type: ignore
               phone_number='61993113326', birth_date='10/11/1978'),
    ]


@pytest.fixture()
def entrances(clients):
    return [
        Entrance(clients[0]), # type: ignore
        Entrance(clients[1]), # type: ignore
        Entrance(clients[2]), # type: ignore
    ]


@pytest.fixture()
def database(app, users, clients, entrances):
    """Fixture que retorna a instância do banco de dados."""

    test_db.session.add_all(users)
    test_db.session.add_all(clients)
    test_db.session.add_all(entrances)
    test_db.session.commit()

    yield test_db


@pytest.fixture()
def client(app):
    """Fixture que retorna o cliente - agente para as requisições nas rotas."""
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
