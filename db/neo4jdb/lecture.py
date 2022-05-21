from pydantic import BaseModel


class LectureCreate(BaseModel):
    title: str
    description: str
    index: int
    courseName: str | None
    resourceName: str | None


class LectureUpdate(BaseModel):
    description: str
    index: int
    courseName: str | None
    resourceName: str | None
