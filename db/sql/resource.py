from . models import MyMixin, Base
from sqlalchemy import Column, String
from sqlalchemy_serializer import SerializerMixin

class Resource(Base, MyMixin, SerializerMixin):
    # TODO: replace by Enum
    type = Column(String(45), nullable=False)
    name = Column(String(100), nullable=False)
    uri = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f'''<Resource(id={self.id}, name={self.name}, uri={self.uri}>'''