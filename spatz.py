from webob import Request, Response


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

        # search for path and handler
        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response

        self.default_response(response)
        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found."

        return response
