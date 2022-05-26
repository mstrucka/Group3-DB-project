from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    description: str
    level: int
    price: float
    onSale: bool
    isCourseOfTheDay: bool | None
    teacherName: str | None
    lectureName: str | None


class CourseUpdate(BaseModel):
    description: str
    level: int
    price: float
    onSale: bool
    isCourseOfTheDay: bool | None
    teacherName: str | None
    lectureName: str | None

