from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    name: str
    email: str
    born: int
    password: str
    isStudent: bool | None
    courseName: str | None


class UserUpdateSchema(BaseModel):
    born: int | None
    courseName: str | None
