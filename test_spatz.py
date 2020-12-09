import pytest

from spatz import Spatz


@pytest.fixture
def app():
    return Spatz()


@pytest.fixture
def client(app):
    return app.test_session()


def test_basic_route_adding(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello"


def test_route_overlap_throws_exception(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello"

    with pytest.raises(AssertionError):    
        @app.route("/home")
        def home2(req, resp):
            resp.text = "Hello"


def test_spatz_test_client_send_requests(app, client):
    RESPONSE_TEXT = "Great Work"

    @app.route("/hey")
    def groovy(req, resp):
        resp.text = RESPONSE_TEXT
    
    assert client.get("http://testserver/hey").text == RESPONSE_TEXT


def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hello, {name}"
    
    assert client.get("http://testserver/john").text == "hello, john"
    assert client.get("http://testserver/ashley").text == "hello, ashley"
