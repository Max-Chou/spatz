# Spatz

*Spatz* German word: "Sparrow".

Spatz is a micro WSGI Web framework for learning purposes.

## Features

* Route
    * Reigster Custom Handlers
    * Parameterized URL
    * Class-Based Handlers
    * Default Response
        * Not Found 404
    * Error Handling

    The app have to dispatch the requests to the handlers correspond to the URLs and HTTP methods. Moreover, the app also have to handle errors from both clients(4XX) or servers(5XX).

* Template Engine


* Static Files

* Middleware


## TODOs

There are two approaches for the future developments. Should I add the features in the framework like Django, or develop many extensions like Flask?

* Session/Cookies
    * Server-Side Session vs Client-Side Session

* Cache

* Database

* Authentication

* Command Line Tools

## Dependency

* [WebOb](https://docs.pylonsproject.org/projects/webob/en/stable/index.html) - HTTP request and response for WSGI app.

* [Parse](https://github.com/r1chardj0n3s/parse) - Parse the path based on the Python format() syntax.

* [Requests](https://github.com/psf/requests) - Send HTTP Requests.

* [WSGI Transport Adapter for Requests](https://github.com/seanbrant/requests-wsgi-adapter) - Create a simple client for testing.

* [Jinja 2](https://jinja.palletsprojects.com/en/2.11.x/) - Template Engine.

* [WhiteNoise](http://whitenoise.evans.io/en/stable/) - Serve Static Files.


## Reference

* [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)

* [Django](https://www.djangoproject.com/)

* [Tornado](https://www.tornadoweb.org/en/stable/)

* [testdriven.io](https://testdriven.io/blog/) - *many useful infos about web development in python*


#### Development Guides

You will know the most famous WSGI frameworks like Django and Flask having the similar features. But of course, they have lots of features to meet most needs and friendly to most web developers.

The project is not to develop a new Flask or Django framework, but to understand how to develop the good frameworks and libraries and how to add a feature to them. The latest ASGI framework still lack 

If you want to develop web applications in other languages like Go, PHP, Rust, Javascript(React.js or Express.js), they follow the same patterns and architectures.

##### Web Development in Python

Basically, you need a **WSGI server** and a **WSGI application** to build the web application in Python. WSGI servers handle the TCP connections to the clients and send HTTP requests to the WSGI applications. WSGI handles the requests, make the responses, and send them back to the WSGI servers.

WSGI servers for productions

* gunicorn
* uwsgi

WSGI frameworks

* Django
* Flask

But WSGI applications are a single synchronous callable which doesn't allow for long-lived connections like long-poll HTTP and WebSocket. Therefore, ASGI was born and most developer moves to FastAPI or Django/Channel. 

ASGI servers

* Uvicorn

ASGI frameworks

* Django/Channels

* FastAPI

Both frameworks and servers

* Tornado

##### Library vs Framework

The library is the bundle of functions and objects. You use them to build the applications, but you don't know the procedures and how to combine them to an application. On the other hand, the framework combines the functions and objects to the real application. The developers just need to modify some objects and functions and customize it.

The example, you can buy a furniture from Ikea and do some DIY stuffs from the manuals. Or you can just buy the chainshaws, hammers and tools to build a furniture. (Even more, like Minecraft you have build your own tools...) Of course, the funitures from Ikea are much cheaper than ones from the professional carpenters.

The other example is Flask and Werkzeug. Flask is built on top of Werkzeug and itsdangerous. Django has its own libraries and modules.
