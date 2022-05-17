from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password_hash: str
    dob: str
    school: str | None = None
    headline: str | None = None
    education: str | None = None
    is_student: bool
    description: str | None = None