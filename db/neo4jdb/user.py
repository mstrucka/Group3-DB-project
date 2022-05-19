from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    name: str
    email: str
    born: int
    password_hash: str
    courseName: str | None


class UserUpdateSchema(BaseModel):
    email: str
    born: int
    password_hash: str
