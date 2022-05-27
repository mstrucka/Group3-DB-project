from pydantic import BaseModel


class PaymentCreate(BaseModel):
    price: float
    courseName: str | None
    studentName: str | None
