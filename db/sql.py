from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# MySQL connection opened, global Session exposed
engine = create_engine('mysql+mysqldb://root:root@localhost/mydb', echo=True, future=True)

Session = sessionmaker(engine)