from pydantic import BaseModel, Field
from api.controller.mongo.PyObjectId import PyObjectId
from bson.objectid import ObjectId

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
    mongo_id: PyObjectId | None = Field(alias='_id')
    id: int | None = None
    password_hash: str
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}