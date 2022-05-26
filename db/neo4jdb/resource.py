from pydantic import BaseModel


class ResourceCreate(BaseModel):
    name: str
    uri: str
    lectureName: str | None


class ResourceUpdate(BaseModel):
    uri: str
    lectureName: str | None
