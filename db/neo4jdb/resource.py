from pydantic import BaseModel


class ResourceCreateSchema(BaseModel):
    id: str
    name: str
    uri: str
    lectureName: str | None


class ResourceUpdateSchema(BaseModel):
    uri: str
    lectureName: str | None
