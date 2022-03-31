from . models import MyMixin, Base
from sqlalchemy import Column, Integer, String, Date, Boolean, Numeric
from sqlalchemy_serializer import SerializerMixin

class Course(MyMixin, SerializerMixin, Base):
    title = Column(String(45), nullable=False)
    description = Column(String(150), nullable=False)
    level = Column(Integer)
    price = Column(Numeric(7, 2), nullable=False)
    platform_sale = Column(Boolean)
    category = Column(String(45))

    def __repr__(self) -> str:
        return f'''<Course(id={self.id}, title={self.title}>'''