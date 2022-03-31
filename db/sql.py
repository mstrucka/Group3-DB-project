from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

# MySQL connection opened, global Session exposed
engine = create_engine('mysql+mysqldb://root:root@localhost/dbfordevs', echo=True, future=True)
Base.metadata.create_all(engine)

Session = sessionmaker(engine)