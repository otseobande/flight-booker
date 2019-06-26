import pytest
from api.app import app, db

@pytest.fixture
def client():
    app.Testing = True
    client = app.test_client()

    yield client

    db.connection.drop_database('test')

