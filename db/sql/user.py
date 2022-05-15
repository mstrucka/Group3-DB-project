from . models import MyMixin, Base
from sqlalchemy import Column, String, Date, Boolean
from sqlalchemy_serializer import SerializerMixin
from pydantic import BaseModel
class User(Base, MyMixin, SerializerMixin):
    #serialize_rules = ('-password_hash',)

    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    school = Column(String(100))
    headline = Column(String(100))
    education = Column(String(100))
    is_student = Column(Boolean, nullable=False)
    description = Column(String(250))

    def __repr__(self) -> str:
        return f'''<User(id={self.id}, firstname={self.firstname}, lastname={self.lastname}>'''