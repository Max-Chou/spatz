from webob import Request, Response


class Spatz():

    def __call__(self, environ, start_response):

        request = Request(environ)

        response = Response()
        response.text = "Hello, World!"

        return response(environ, start_response)
