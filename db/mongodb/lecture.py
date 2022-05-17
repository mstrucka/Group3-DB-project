from pydantic import BaseModel, Field
from api.controller.mongo.PyObjectId import PyObjectId
from bson.objectid import ObjectId

class LectureSchema(BaseModel):
    id: PyObjectId = Field(..., alias='_id')
    title: str
    description: str
    index: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True #required for the _id 
        json_encoders = {ObjectId: str}