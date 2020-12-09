import inspect
from webob import Request, Response
from parse import parse
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

class Spatz():

    def __init__(self):

        self.routes = {}

    def __call__(self, environ, start_response):

        request = Request(environ)

        response = self.handle_request(request)
        
        return response(environ, start_response)


    def route(self, path):
        """Register the function to the given path

        :param path: url path
        :type path: string
        """
        # if path in self.routes:
        #     raise AssertionError("Such route already exists.")
        assert path not in self.routes, "Such route already exists."

        def wrapper(handler):
            self.routes[path] = handler
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

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if not handler:
                    raise AttributeError("Method not allowed", request.method)

            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response


    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found."

        return response


    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)

            if parse_result:
                return handler, parse_result.named

        return None, None


    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session
