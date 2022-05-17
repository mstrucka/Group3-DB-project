

from typing import List
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from api.controller.mongo.PyObjectId import PyObjectId
from db.mongodb.lecture import LectureSchema

class CourseSchema(BaseModel):
    id: PyObjectId | None = Field(default_factory=PyObjectId, alias='_id')
    title: str
    description: str
    level: int | None
    price: float
    platform_sale: bool | None
    category: str | None
    lecturer_id: PyObjectId | None
    lectures: List[LectureSchema] | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True #required for the _id 
        json_encoders = {ObjectId: str}

class CourseCreateSchema(BaseModel):
    title: str
    description: str
    level: int | None
    price: float
    platform_sale: bool | None
    category: str | None
    lecturer_id: PyObjectId | None
    lectures: List[LectureSchema] | None

class CourseEditSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    title: int | None = None
    price: float | None = None
    platform_sale: bool | None = None
    category: str | None = None
    lecturer_id: PyObjectId | None = None
    lectures: List[LectureSchema] | None = None