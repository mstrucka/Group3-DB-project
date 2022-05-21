from pydantic import BaseModel


class PaymentCreate(BaseModel):
    id: str
    price: float
    courseName: str | None
    studentName: str | None
