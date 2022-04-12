import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.sql.models import Base
from . import user, course, lecture, payment, resource, enrollment

def local_db_setup():
    db_url = f'mysql+mysqldb://{os.getenv("SQL_USER")}:{os.getenv("SQL_PASS")}@{os.getenv("SQL_HOST")}:{os.getenv("SQL_PORT")}/{os.getenv("SQL_DB")}'
    engine = create_engine(db_url, future=True, echo=True)

    # Drop tables
    Base.metadata.drop_all(engine, checkfirst=True)

    # Add tables
    Base.metadata.create_all(engine)

    # Global session to use when querying
    global Session
    Session = sessionmaker(engine)

    # populate db
    with Session.begin() as session:
        with open('test-data.sql') as file:
            query = text(file.read())
            session.execute(query)

def prod_db_setup():
    db_url = os.environ.get('JAWSDB_URL')
    engine = create_engine(db_url, future=True, echo=True)

    # Global session to use when querying
    global Session
    Session = sessionmaker(engine)


if os.environ.get('APP_LOCATION') == 'heroku':
    prod_db_setup()
else:
    local_db_setup()




