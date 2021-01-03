import os
import inspect
from datetime import datetime, timedelta

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request
from werkzeug.exceptions import NotFound, HTTPException, MethodNotAllowed
from parse import parse
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise

from sqlalchemy.ext.declarative import declarative_base

from .middleware import Middleware
from .response import Response
from .database import Database
from .session import ClientSession


class Spatz:
    """The Spatz WSGI Application Class.
    Including Jinga Template Engine, Whitenoise Static files management, SQLAlchemy ORM...

    You can replace the template engine or static files directory if you know well Jinga2 Template and whitenoise.
    """

    # the default configuration
    default_config = {
        "ENV": None,
        "DEBUG": None,
        "SECRET_KEY": None,
        "SESSION_COOKIE_NAME": "session",
        "SESSION_COOKIE_DOMAIN": None,
        "SESSION_COOKIE_PATH": None,
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SECURE": False,
        "SESSION_COOKIE_SAMESITE": None,
        "PERMANENT_SESSION_LIFETIME": timedelta(days=1),
    }

    def __init__(self, templates_dir="templates", static_dir="static"):

        self.routes = Map()
        self.handlers = {}

        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )
        self.exception_handler = {}
        self.whitenoise = WhiteNoise(
            self.wsgi_app, root=static_dir, prefix="static/", max_age=31536000
        )
        self.middleware = Middleware(self)
        self.db = Database(self)
        self.config = self.default_config.copy()

        # session interface
        self.SessionInterface = ClientSession

        # cache interface
        self.CacheInterface = None

    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)

    def wsgi_app(self, environ, start_response):
        return self.middleware(environ, start_response)

    def add_route(self, rule, handler, endpoint=None, methods=["GET"]):
        """Add a URL Rule.

        :param url: the URL rule.
        :type url: str
        :param handler: the function handling a request
        :type handler: callable
        :param endpoint: the endpoint for registered URL rule, defaults to None
        :type endpoint: str, optional
        :param methods: allowed methods, defaults to ["GET"]
        :type methods: list, optional
        """

        # check if the rule exists
        for r in self.routes.iter_rules():
            if rule == r.rule:
                raise AssertionError("Such URL already exists.")

        if endpoint is None:
            endpoint = handler.__name__

        # class-based handler
        if inspect.isclass(handler):
            for method in ["post", "put", "delete"]:
                if hasattr(handler, method):
                    methods.append(method)

        rule = Rule(rule, endpoint=endpoint, methods=methods)
        self.routes.add(rule)
        self.handlers[endpoint] = handler

    def route(self, rule, **kwargs):
        def wrapper(handler):
            self.add_route(rule, handler, **kwargs)
            return handler

        return wrapper

    def handle_request(self, request):
        """Handle requests and dispatch the requests to view functions

        :param request: requests from clients
        :type request: webob.Request
        :return: responses from view functions
        :rtype: webob.Response
        """
        response = Response()
        response.render = self.render

        urls = self.routes.bind_to_environ(request.environ)
        try:
            endpoints, kwargs = urls.match()
            handler = self.handlers[endpoints]

            # class-based handler
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
            if not handler:
                raise MethodNotAllowed()

            handler(request, response, **kwargs)

        except HTTPException as e:
            return e

        return response

    def render(self, template_name, context=None):
        if context is None:
            context = {}
        return self.templates_env.get_template(template_name).render(**context)

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found."

        return response

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
