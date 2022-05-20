from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    name: str
    email: str
    born: int
    password: str
    isStudent: bool
    courseName: str | None


class UserUpdateSchema(BaseModel):
    born: int | None
