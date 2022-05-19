
from datetime import datetime
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from api.controller.mongo.PyObjectId import PyObjectId

class PaymentSchema(BaseModel):
    id: PyObjectId = Field(alias='_id')
    date: str
    is_refund: bool
    total: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True #required for the _id 
        json_encoders = {ObjectId: str}


