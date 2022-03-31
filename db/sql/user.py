from . models import MyMixin, Base
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy_serializer import SerializerMixin

class User(Base, MyMixin, SerializerMixin):
    firstName = Column(String(45), nullable=False)
    lastName = Column(String(45), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(45), nullable=False)
    dob = Column(Date, nullable=False)
    school = Column(String(100))
    headline = Column(String(100))
    education = Column(String(100))
    isStudent = Column(Boolean, nullable=False)
    description = Column(String(250))

    def __repr__(self) -> str:
        return f'''<User(id={self.id}, firstName={self.firstName}, lastName={self.lastName}>'''