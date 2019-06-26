import pytest
from decouple import config as env_config
from api.app import app, db

@pytest.fixture
def client():
    app.Testing = True
    client = app.test_client()

    yield client

    database_url = env_config('MONGO_URL')
    database_name = database_url.split('/')[-1]

    db.connection.drop_database(database_name)

