import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.sql.models import Base
from . import user, course, lecture, payment, resource

# MySQL connection opened, global Session exposed
engine = create_engine(
    f'mysql+mysqldb://{os.getenv("SQL_USER")}:{os.getenv("SQL_PASS")}@{os.getenv("SQL_HOST")}:{os.getenv("SQL_PORT")}/{os.getenv("SQL_DB")}'
    , echo=True, future=True)

# Drop tables
Base.metadata.drop_all(engine, checkfirst=True)

# Add tables
Base.metadata.create_all(engine)

# populate db
""" with engine.connect() as conn:
    with open('sql-scripts\data_inserts.sql') as file:
        query = text(file.read())
        conn.execute(query) """

Session = sessionmaker(engine)


