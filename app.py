from spatz import Spatz
from spatz import Middleware

app = Spatz()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"


@app.route("/hello/{name}")
def hello(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"
    
    def post(self, req, resp):
        resp.text = "Create a Book Object"


def curse(req, resp):
    resp.text = "Curse you!"


app.add_route("/curse", curse)


@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template(
        "index.html", context={"name": "Spatz", "title": "Best Framework"})


@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be used.")


# custom middleware
class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)
    
    def process_response(self, req, res):
        print("Processing response", req.url)

app.add_middleware(SimpleCustomMiddleware)


@app.route("/json")
def json_handler(req, resp):
    resp.json = {"name": "data", "type": "JSON"}

@app.route("/text")
def text_handler(req, resp):
    resp.text = "This is a simple text"

