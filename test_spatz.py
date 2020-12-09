import pytest

from spatz import Spatz


FILE_DIR = "css"
FILE_NAME = "main.css"
FILE_CONTENTS = "body {background-color: red}"

# helpers
def _create_static(static_dir):
    asset = static_dir.mkdir(FILE_DIR).join(FILE_NAME)
    asset.write(FILE_CONTENTS)

    return asset

# tests
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


def test_template(app, client):
    @app.route("/html")
    def html_handler(req, resp):
        resp.body = app.template("index.html", context={"title": "Some Title", "name": "Some Name"}).encode()

    response = client.get("http://testserver/html")

    assert "text/html" in response.headers["Content-Type"]
    assert "Some Title" in response.text
    assert "Some Name" in response.text


def test_custom_exception_handler(app, client):
    def on_exception(req, resp, exc):
        resp.text = "AttributeErrorHappened"
    
    app.add_exception_handler(on_exception)

    @app.route("/")
    def index(req, resp):
        raise AttributeError()

    response = client.get("http://testserver/")

    assert response.text == "AttributeErrorHappened"


def test_assets_are_served(tmpdir_factory):
    static_dir = tmpdir_factory.mktemp("static")
    _create_static(static_dir)
    app = Spatz(static_dir=str(static_dir))
    client = app.test_session()

    response = client.get(f"http://testserver/{FILE_DIR}/{FILE_NAME}")

    assert response.status_code == 200
    assert response.text == FILE_CONTENTS


# def test_middleware_methods_are_called(app, client):
#     process_request_called = False
#     process_response_called = False