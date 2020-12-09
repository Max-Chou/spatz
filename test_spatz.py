import pytest

from spatz import Spatz


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


def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not Found."


def test_class_based_handler_get(app, client):
    response_text = "this is a get request"

    @app.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = response_text
    
    assert client.get("http://testserver/book").text == response_text


def test_class_based_handler_post(app, client):
    response_text = "this is a post request"

    @app.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text

    assert client.post("http://testserver/book").text == response_text


def test_class_based_handler_not_allowed_method(app, client):
    @app.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = "no way!"

    with pytest.raises(AttributeError):
        client.get("http://testserver/book")


def test_alternative_route(app, client):
    response_text = "haha"

    def home(req, resp):
        resp.text = response_text
    
    app.add_route("/alternative", home)

    assert client.get("http://testserver/alternative").text == response_text
