from pydantic import BaseModel


class PaymentCreateSchema(BaseModel):
    id: str
    price: float
    courseName: str | None
    studentName: str | None
