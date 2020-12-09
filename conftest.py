import pytest

from spatz import Spatz


@pytest.fixture
def app():
    return Spatz()


@pytest.fixture
def client(app):
    return app.test_session()
