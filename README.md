# Spatz

![purpose](https://img.shields.io/badge/purpose-learning-green.svg)
![PyPI](https://img.shields.io/pypi/v/spatz.svg)

*Spatz* German word: "Sparrow".

Spatz is a micro WSGI Web framework for learning purposes.


## Installation

```shell
pip install spatz
```

## How to use it

```python
from spatz import Spatz

app = Spatz()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"


@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template(
        "index.html", context={"name": "Spatz", "title": "Best Framework"})
```

### Unit Tests

The recommended way of writing unit tests is with [pytest](https://docs.pytest.org/en/latest/). There are two built in fixtures
that you may want to use when writing unit tests with Spatz. The first one is `app` which is an instance of the main `Spatz` class:

```python
def test_route_overlap_throws_exception(app):
    @app.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    with pytest.raises(AssertionError):
        @app.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home2."
```

The other one is `client` that you can use to send HTTP requests to your handlers. It is based on the famous [requests](http://docs.python-requests.org/en/master/) and it should feel very familiar:

```python
def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
```

## Templates

The default folder for templates is `templates`. You can change it when initializing the main `Spatz()` class:

```python
app = Spatz(templates_dir="templates_dir_name")
```

Then you can use HTML files in that folder like so in a handler:

```python
@app.route("/show/template")
def handler_with_template(req, resp):
    resp.html = app.template(
        "example.html", context={"title": "Awesome Framework", "body": "welcome to the future!"})
```

## Static Files

Just like templates, the default folder for static files is `static` and you can override it:

```python
app = Spatz(static_dir="static_dir_name")
```

Then you can use the files inside this folder in HTML files:

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>

  <link href="/static/main.css" rel="stylesheet" type="text/css">
</head>

<body>
    <h1>{{body}}</h1>
    <p>This is a paragraph</p>
</body>
</html>
```

### Middleware

You can create custom middleware classes by inheriting from the `spatz.Middleware` class and overriding its two methods that are called before and after each request:

```python
from spatz import Spatz
from spatz import Middleware


app = Spatz()


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Before dispatch", req.url)

    def process_response(self, req, res):
        print("After dispatch", req.url)


app.add_middleware(SimpleCustomMiddleware)
```




## TODOs

There are two approaches for the future developments. Should I add the features in the framework like Django, or develop many extensions like Flask?

* Session/Cookies
    * Server-Side Session vs Client-Side Session

* Cache

* Database

* Authentication

* Command Line Tools

## Dependency

* [WebOb](https://docs.pylonsproject.org/projects/webob/en/stable/index.html) - HTTP request and response for WSGI app.

* [Parse](https://github.com/r1chardj0n3s/parse) - Parse the path based on the Python format() syntax.

* [Requests](https://github.com/psf/requests) - Send HTTP Requests.

* [WSGI Transport Adapter for Requests](https://github.com/seanbrant/requests-wsgi-adapter) - Create a simple client for testing.

* [Jinja 2](https://jinja.palletsprojects.com/en/2.11.x/) - Template Engine.

* [WhiteNoise](http://whitenoise.evans.io/en/stable/) - Serve Static Files.


## Reference

* [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)

* [Django](https://www.djangoproject.com/)

* [Tornado](https://www.tornadoweb.org/en/stable/)

* [testdriven.io](https://testdriven.io/blog/) - *many useful infos about web development in python*


#### Development Guides

You will know the most famous WSGI frameworks like Django and Flask having the similar features. But of course, they have lots of features to meet most needs and friendly to most web developers.

The project is not to develop a new Flask or Django framework, but to understand how to develop the good frameworks and libraries and how to add a feature to them. The latest ASGI framework still lack 

If you want to develop web applications in other languages like Go, PHP, Rust, Javascript(React.js or Express.js), they follow the same patterns and architectures.

##### Web Development in Python

Basically, you need a **WSGI server** and a **WSGI application** to build the web application in Python. WSGI servers handle the TCP connections to the clients and send HTTP requests to the WSGI applications. WSGI handles the requests, make the responses, and send them back to the WSGI servers.

WSGI servers for productions

* gunicorn
* uwsgi

WSGI frameworks

* Django
* Flask

But WSGI applications are a single synchronous callable which doesn't allow for long-lived connections like long-poll HTTP and WebSocket. Therefore, ASGI was born and most developer moves to FastAPI or Django/Channel. 

ASGI servers

* Uvicorn

ASGI frameworks

* Django/Channels

* FastAPI

Both frameworks and servers

* Tornado

##### Library vs Framework

The library is the bundle of functions and objects. You use them to build the applications, but you don't know the procedures and how to combine them to an application. On the other hand, the framework combines the functions and objects to the real application. The developers just need to modify some objects and functions and customize it.

The example, you can buy a furniture from Ikea and do some DIY stuffs from the manuals. Or you can just buy the chainshaws, hammers and tools to build a furniture. (Even more, like Minecraft you have build your own tools...) Of course, the funitures from Ikea are much cheaper than ones from the professional carpenters.

The other example is Flask and Werkzeug. Flask is built on top of Werkzeug and itsdangerous. Django has its own libraries and modules.
