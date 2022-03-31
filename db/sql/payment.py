from . models import MyMixin, Base
from sqlalchemy import Column, Numeric, Boolean, DateTime
from sqlalchemy_serializer import SerializerMixin

class Payment(Base, MyMixin, SerializerMixin):
    date = Column(DateTime, nullable=False)
    is_refund = Column(Boolean, nullable=False)
    total = Column(Numeric(7, 2), nullable=False)
    

    def __repr__(self) -> str:
        return f'''<Payment(id={self.id}, date={self.date}, total={self.total}>'''