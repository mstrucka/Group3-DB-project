from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    born: int
    password: str
    isStudent: bool | None
    courseName: str | None


class UserUpdate(BaseModel):
    born: int | None
    courseName: str | None
