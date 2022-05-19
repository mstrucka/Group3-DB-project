from pydantic import BaseModel
from pydantic.validators import datetime


class PaymentCreateSchema(BaseModel):
    id: str
    date: datetime
    price: float
    courseName: str
    studentName: str
