import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.sql.models import Base
from . import user, course, lecture, payment, resource, enrollment
# MySQL connection opened, global Session exposed
engine = create_engine(
    f'mysql+mysqldb://{os.getenv("SQL_USER")}:{os.getenv("SQL_PASS")}@{os.getenv("SQL_HOST")}:{os.getenv("SQL_PORT")}/{os.getenv("SQL_DB")}'
    , echo=False, future=True)

# Drop tables
Base.metadata.drop_all(engine, checkfirst=True)

# Add tables
Base.metadata.create_all(engine)

# Global session to use when querying
Session = sessionmaker(engine)

# populate db
with Session.begin() as session:
    with open('test-data.sql') as file:
        query = text(file.read())
        session.execute(query)

