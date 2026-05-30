import pytest
from model_bakery import baker


@pytest.fixture
def logged_in_client(client, db):
    user = baker.make("core.User")
    client.force_login(user)
    return client
