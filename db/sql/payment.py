from datetime import datetime
from typing import List

from pydantic import BaseModel
from . models import MyMixin, Base
from sqlalchemy import Column, Numeric, Boolean, DateTime
from sqlalchemy_serializer import SerializerMixin

class Payment(Base, MyMixin, SerializerMixin):
    date = Column(DateTime, nullable=False, default=datetime.now())
    is_refund = Column(Boolean, nullable=False, default=False)
    total = Column(Numeric(7, 2), nullable=False)

    def __repr__(self) -> str:
        return f'''<Payment(id={self.id}, date={self.date}, total={self.total}>'''

class PaymentEdit(BaseModel):
    date: str | None = None
    is_refund: bool | None = None
    total: float | None = None
class PaymentCreate(BaseModel):
    course_ids: List[int | str]