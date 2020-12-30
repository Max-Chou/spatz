from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .middleware import Middleware

Model = declarative_base()

class Database:
    def __init__(self, app):
        self.app = app
        self.Model = Model

    def init_db(self):
        """Initialize the database abstraction layer, creating the session, the database schema, the middleware.

        """
        database_uri = self.app.config.get("DATABASE_URI", "sqlite:///data.sqlite")
        self.engine = create_engine(database_uri)
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine))
        self.Model.query = self.session.query_property()
        self.Model.metadata.create_all(bind=self.engine)

        class DatabaseMiddleware(Middleware):
            def process_request(self, req):
                req.db_session = self.app.db.session

            def process_response(self, req, res):
                req.db_session.remove()

        self.app.add_middleware(DatabaseMiddleware)
