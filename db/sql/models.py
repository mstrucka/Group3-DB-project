from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr
from sqlalchemy import Column, Integer

@declarative_mixin
class MyMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__= {'always_refresh': True}

    id = Column(Integer, primary_key=True)

Base = declarative_base()



