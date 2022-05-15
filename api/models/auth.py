from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class User(BaseModel):
    email: str
    firstname: str
    lastname: str
    dob: str
    school: str | None = None
    headline: str | None = None
    education: str | None = None
    is_student: bool
    description: str | None = None

class UserCreate(User):
    password: str

class UserEdit(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    dob: str | None = None
    school: str | None = None
    headline: str | None = None
    education: str | None = None
    description: str | None = None

class UserInDB(User):
    id: int
    password_hash: str