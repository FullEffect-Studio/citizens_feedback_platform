import pytest

from web.app import create_app


@pytest.fixture
def app():
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    # app = create_app()
    app.testing = True
    client = app.test_client()

    yield client