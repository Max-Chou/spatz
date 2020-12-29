from werkzeug.wrappers import Request

class Middleware:
    def __init__(self, app):
        self.app = app
    
    def add(self, middleware_cls):
        self.app = middleware_cls(self.app)
    
    def process_request(self, req):
        pass

    def process_response(self, req, res):
        pass

    def handle_request(self, req):

        # handle request before the handlers
        self.process_request(req)
        res = self.app.handle_request(req)

        self.process_response(req, res)

        return res
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)
