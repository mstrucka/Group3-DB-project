from . models import MyMixin, Base
from sqlalchemy import Column, SmallInteger, String
from sqlalchemy_serializer import SerializerMixin

class Lecture(Base, MyMixin, SerializerMixin):
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    # could also be mysql.TINYINT
    index = Column(SmallInteger(2), nullable=False)
    

    def __repr__(self) -> str:
        return f'''<Lecture(id={self.id}, title={self.title}, index={self.index}>'''