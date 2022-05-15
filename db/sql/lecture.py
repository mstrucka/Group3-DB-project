from . models import MyMixin, Base
from . association_tables import lecture_resources
from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from pydantic import BaseModel

class Lecture(Base, MyMixin, SerializerMixin):
    title = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)
    # could also be mysql.TINYINT
    index = Column(SmallInteger, nullable=False)

    resources = relationship('Resource', secondary=lecture_resources)
    
    def __repr__(self) -> str:
        return f'''<Lecture(id={self.id}, title={self.title}, index={self.index}>'''

class LectureBase(BaseModel):
    title: str | None
    description: str | None
    index: int | None

class LectureEdit(LectureBase):
    pass
class LectureCreate(LectureBase):
    pass