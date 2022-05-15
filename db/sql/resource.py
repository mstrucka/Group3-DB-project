from . models import MyMixin, Base
from sqlalchemy import Column, String
from sqlalchemy_serializer import SerializerMixin
from pydantic import BaseModel

class Resource(Base, MyMixin, SerializerMixin):
    # TODO: replace by Enum
    type = Column(String(45), nullable=False)
    name = Column(String(100), nullable=False)
    uri = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f'''<Resource(id={self.id}, name={self.name}, uri={self.uri}>'''

class ResourceEdit(BaseModel):
    type: str | None = None
    name: str | None = None
    uri: str | None = None

class ResourceCreate(BaseModel):
    type: str
    name: str
    uri: str
    lecture_id: int