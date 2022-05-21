from pydantic import BaseModel


class CourseCreateSchema(BaseModel):
    id: int | None
    title: str
    description: str
    level: int
    price: float
    onSale: bool
    isCourseOfTheDay: bool | None
    teacherName: str | None
    lectureName: str | None


class CourseUpdateSchema(BaseModel):
    description: str
    level: int
    price: float
    onSale: bool
    isCourseOfTheDay: bool | None
    teacherName: str | None
    lectureName: str | None

