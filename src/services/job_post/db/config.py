from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2

class DBConnectionHandler:
    """
    PostgreSQL database connection using SQLAlchemy.
    """

    def __init__(self, db_url: str) -> None:
        self.__connection_string = db_url
        self.session = None

    def get_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def __enter__(self):
        engine = create_engine(self.__connection_string)
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.session.close()
