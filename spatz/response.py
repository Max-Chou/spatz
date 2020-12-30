import json

from werkzeug.wrappers import Response as WerkzeugResponse


class Response(WerkzeugResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json = None
        self.html = None
        self.text = None
    
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


# class Response:
#     def __init__(self):
#         self.json = None
#         self.html = None
#         self.text = None
#         self.content_type = None
#         self.body = ''
#         self.status_code = 200
#         self._response = WerkzeugResponse()


#     def __call__(self, environ, start_response):
#         self.set_body_and_content_type()

#         #response = WerkzeugResponse(
#         #    self.body, content_type=self.content_type , status=self.status_code
#         #)
#         self._response.data = self.body
#         self._response.content_type = self.content_type

#         return self._response(environ, start_response)

#     def set_


#     def set_body_and_content_type(self):
#         if self.json:
#             self.body = json.dumps(self.json)
#             self.content_type = "application/json"
        
#         if self.html:
#             self.body = self.html
#             self.content_type = "text/html"
        
#         if self.text:
#             self.body = self.text
#             self.content_type = "text/plain"
        