from pydantic import BaseModel


class ResourceCreateSchema(BaseModel):
    title: str
    description: str
    index: int
    lectureName: str


class ResourceUpdateSchema(BaseModel):
    title: str
    description: str
    index: int
    lectureName: str
