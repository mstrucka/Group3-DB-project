from pydantic import BaseModel


class LectureCreateSchema(BaseModel):
    title: str
    description: str
    index: int
    courseName: str | None
    resourceName: str | None


class LectureUpdateSchema(BaseModel):
    description: str
    index: int
    courseName: str | None
    resourceName: str | None
