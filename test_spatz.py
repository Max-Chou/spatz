import pytest

from spatz import Spatz


@pytest.fixture
def spatz():
    return Spatz()


def test_basic_route_adding(spatz):
    @spatz.route("/home")
    def home(req, resp):
        resp.text = "Hello"
