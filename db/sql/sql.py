import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.sql.models import Base
from . import *


def local_db_setup():
    db_url = f'mysql+mysqldb://{os.getenv("SQL_USER")}:{os.getenv("SQL_PASS")}@{os.getenv("SQL_HOST")}:{os.getenv("SQL_PORT")}/{os.getenv("SQL_DB")}'
    engine = create_engine(db_url, future=True, echo=True)

    # Drop tables
    Base.metadata.drop_all(engine, checkfirst=True)

    # Add tables
    Base.metadata.create_all(engine, checkfirst=True)

    # Global session to use when querying
    rootSession = sessionmaker(engine)

    # populate db
    with rootSession.begin() as session:
        with open('./sql-scripts/test-data.sql') as file, \
                open('./sql-scripts/event-routine-trigger-view-privileges.sql') as file2:
            query = text(file.read())
            session.execute(query)
            query = text(file2.read())
            session.execute(query)

    engine.dispose()
    db_url = f'mysql+mysqldb://{os.getenv("SQL_APIUSER")}:{os.getenv("SQL_APIPASS")}@{os.getenv("SQL_HOST")}:{os.getenv("SQL_PORT")}/{os.getenv("SQL_DB")}'
    engine = create_engine(db_url, future=True, echo=True)
    global Session
    Session = sessionmaker(engine)


def prod_db_setup():
    db_url = os.environ.get('DATABASE_URL')
    engine = create_engine(db_url, future=True, echo=True)

    # Global session to use when querying
    global Session
    Session = sessionmaker(engine)


if os.environ.get('APP_LOCATION') == 'heroku':
    prod_db_setup()
else:
    local_db_setup()
