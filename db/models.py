from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr
from sqlalchemy import Column, Integer, String, Date, Boolean

@declarative_mixin
class MyMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__= {'always_refresh': True}

    id = Column(Integer, primary_key=True)

Base = declarative_base()

class User(MyMixin, Base):
    firstName = Column(String(45), nullable=False)
    lastName = Column(String(45), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(45), nullable=False)
    dob = Column(Date, nullable=False)
    school = Column(String(100))
    headline = Column(String(100))
    education = Column(String(100))
    isStudent = Column(Boolean, nullable=False)
    description = Column(String(250))

    def __repr__(self) -> str:
        return f'''<User(firstName={self.firstName}, lastName={self.lastName}'''

