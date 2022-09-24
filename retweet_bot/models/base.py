import datetime
import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
logger = logging.getLogger(__name__)


def current_time():
    """get current time in string"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class BaseDB:
    def __init__(self, db_name, echo=False, reset=False, init=False):
        """init"""
        engine = create_engine(
            db_name, echo=echo, connect_args={"check_same_thread": False}
        )
        if reset:
            Base.metadata.drop_all(engine)
        if init:
            Base.metadata.create_all(engine)
        self.maker = sessionmaker(bind=engine, autoflush=False)
        self.session = self.maker()

    def __commit(self, session=None):
        """Commits the current db.session, does rollback on failure."""
        session = session or self.session
        try:
            session.commit()
        except IntegrityError:
            session.rollback()

    def add(self, obj, session=None):
        """Adds this model to the db (through db.session)"""
        session = session or self.session
        session.add(obj)
        self.__commit(session)

    def commit(self):
        """commit"""
        self.__commit()
