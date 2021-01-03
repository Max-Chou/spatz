from werkzeug.wrappers import Request
from datetime import datetime, timedelta


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
        self.process_request(req)
        res = self.app.handle_request(req)
        self.process_response(req, res)

        return res

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)


class SessionMiddleware(Middleware):
    def __init__(self, app):
        super().__init__(app)
        self.SessionInterface = app.SessionInterface

    def process_request(self, req):
        session_key = req.cookies.get(self.app.config["SESSION_COOKIE_NAME"])
        req.session = self.SessionInterface(session_key=session_key)

    def process_response(self, req, res):
        expires = datetime.utcnow() + self.app.config["PERMANENT_SESSION_LIFETIME"]
        req.session.save()
        res.set_cookie(
            self.app.config["SESSION_COOKIE_NAME"],
            req.session.session_key,
            expires=expires,
            domain=self.app.config["SESSION_COOKIE_DOMAIN"],
            path=self.app.config["SESSION_COOKIE_PATH"],
            secure=self.app.config["SESSION_COOKIE_SECURE"],
            httponly=self.app.config["SESSION_COOKIE_HTTPONLY"],
        )
