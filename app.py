from spatz import Spatz


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
        "index.html", context={"name": "Spatz", "title": "Best Framework"}
    ).encode()
