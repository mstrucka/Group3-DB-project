from pydantic import BaseModel


class CourseCreateSchema(BaseModel):
    id: int | None
    title: str
    description: str
    level: int
    price: float
    onSale: bool
    isCourseOfTheDay: bool | False
    teacherName: str | None
    lectureName: str | None


class CourseUpdateSchema(BaseModel):
    id: int | None
    description: str
    level: int
    price: float
    onSale: bool
    isCourseOfTheDay: bool | False
    teacherName: str | None
    lectureName: str | None

