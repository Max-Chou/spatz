import json

from werkzeug.wrappers import Response as WerkzeugResponse


class Response(WerkzeugResponse):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json = None
        self.html = None
        self.text = None
        self.app = app
    
    def __call__(self, environ, start_response):
        self.set_body_and_content_type()

        return super().__call__(environ, start_response)


    def set_body_and_content_type(self):
        if self.json:
            self.data = json.dumps(self.json)
            self.content_type = "application/json"
        
        if self.html:
            self.data = self.html
            self.content_type = "text/html"
        
        if self.text:
            self.data = self.text
            self.content_type = "text/plain"


    def render(self, template_name, context=None):
        self.data = self.app.render(template_name, context)
        self.content_type = "text/html"
