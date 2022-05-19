from pydantic import BaseModel


class LectureCreateSchema(BaseModel):
    id: str | None
    title: str
    description: str
    index: int
    courseName: str | None
    resourceName: str | None


class LectureUpdateSchema(BaseModel):
    title: str
    description: str
    index: int
    courseName: str | None
    resourceName: str | None
