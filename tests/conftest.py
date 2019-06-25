import pytest
from api.app import app

@pytest.fixture
def client():
    app.Testing = True
    client = app.test_client()

    yield client
