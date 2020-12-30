import os
import inspect
from datetime import datetime, timedelta

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
from .template import TemplateEnvironment
from .session import ClientSession


class Spatz():
    """The Spatz WSGI Application Class.
    Including Jinga Template Engine, Whitenoise Static files management, SQLAlchemy ORM...

    You can replace the template engine or static files directory if you know well Jinga2 Template and whitenoise.
    """

    # the default configuration
    default_config = {
        'ENV': None,
        'DEBUG': None,
        'SECRET_KEY': None,
        'SESSION_COOKIE_NAME': 'session',
        'SESSION_COOKIE_DOMAIN': None,
        'SESSION_COOKIE_PATH': None,
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_SECURE': False,
        'SESSION_COOKIE_SAMESITE': None,
        'PERMANENT_SESSION_LIFETIME': timedelta(days=1)
    }

    def __init__(self, templates_dir="templates", static_dir="static"):

        self.routes = {}
        self.templates_env = TemplateEnvironment
        self.templates_env.loader = FileSystemLoader(os.path.abspath(templates_dir))
        self.exception_handler = {}
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir, prefix="static/", max_age=31536000)
        self.middleware = Middleware(self)
        self.db = Database(self)
        self.config = self.default_config.copy()
        
        self.SessionInterface = ClientSession


    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)


    def wsgi_app(self, environ, start_response):
        return self.middleware(environ, start_response)


    def add_route(self, path, handler, allowed_methods=None):
        """Add a new view function to the routes

        :param path: url path
        :type path: str
        :param handler: view function
        :type handler: function
        """
        assert path not in self.routes, "Such route already exists."

        #self.routes[path] = handler
        if allowed_methods:
            self.routes[path] = {"handler": handler, "allowed_methods": allowed_methods}
        else:
            self.routes[path] = {"handler": handler, "allowed_methods": ["get"]}


    def route(self, path, allowed_methods=None):
        """Register the function to the given path

        :param path: url path
        :type path: str
        """
        def wrapper(handler):
            self.add_route(path, handler, allowed_methods)
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

        handler_data, kwargs = self.find_handler(request_path=request.path)
        handler = None

        try:
            if handler_data:
                if inspect.isclass(handler_data["handler"]):
                    handler = getattr(handler_data["handler"](), request.method.lower(), None)
                else:
                    if request.method.lower() in handler_data["allowed_methods"]:
                        handler = handler_data["handler"]

                if not handler:
                    raise MethodNotAllowed()

                handler(request, response, **kwargs)
            else:
                raise NotFound()

        except HTTPException as e:
            return e

        return response


    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found."

        return response


    def find_handler(self, request_path):
        for path, handler_data in self.routes.items():
            parse_result = parse(path, request_path)

            if parse_result:
                return handler_data, parse_result.named

        return None, None


    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session


    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler


    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
