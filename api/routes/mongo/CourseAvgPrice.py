from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from api.controller.mongo.PyObjectId import PyObjectId

class CourseAvgPrice(BaseModel):
    lecturer_id: PyObjectId | None = Field(alias='_id')
    avg_price: float | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True #required for the _id 
        json_encoders = {ObjectId: str}