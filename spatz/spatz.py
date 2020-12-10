import os
import inspect

from webob import Request
from webob.exc import HTTPNotFound, HTTPInternalServerError, HTTPMethodNotAllowed
from parse import parse
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise

from .middleware import Middleware
from .response import Response


class Spatz():

    def __init__(self, templates_dir="templates", static_dir="static"):

        self.routes = {}

        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )

        self.exception_handler = None

        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)

        self.middleware = Middleware(self)


    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]

        if path_info.startswith("/static"):
            environ["PATH_INFO"] = path_info[len("/static"):]
            return self.whitenoise(environ, start_response)

        return self.middleware(environ, start_response)


    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)


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
                    raise AttributeError("Method not allowed", request.method)
                    #response = HTTPMethodNotAllowed()

                handler(request, response, **kwargs)
            else:
                # client errors
                response = self.default_response(response)
                # response = HTTPNotFound()

        # server errors
        except Exception as e:
            if not self.exception_handler:
                raise e
            else:
                self.exception_handler(request, response, e)
            # response = HTTPInternalServerError()

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


    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)


    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler


    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
