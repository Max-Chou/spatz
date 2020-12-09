import pytest

from spatz import Spatz


@pytest.fixture
def spatz():
    return Spatz()


def test_basic_route_adding(spatz):
    @spatz.route("/home")
    def home(req, resp):
        resp.text = "Hello"


def test_route_overlap_throws_exception(spatz):
    @spatz.route("/home")
    def home(req, resp):
        resp.text = "Hello"

    with pytest.raises(AssertionError):    
        @spatz.route("/home")
        def home2(req, resp):
            resp.text = "Hello"
