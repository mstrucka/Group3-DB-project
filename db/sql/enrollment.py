from . models import MyMixin, Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from pydantic import BaseModel
from api.controller.mongo.PyObjectId import PyObjectId
from bson.objectid import ObjectId

class Enrollment(Base, MyMixin, SerializerMixin):
    student_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    payment_id = Column(Integer, ForeignKey('payment.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    finished = Column(Boolean, nullable=False, default=False)

    course = relationship('Course', cascade='all, delete')
    payment = relationship('Payment')
    student = relationship('User')

class EnrollmentBase(BaseModel):
    student_id: PyObjectId | None
    course_id: PyObjectId | None
    payment_id: PyObjectId | None
    finished: bool | None = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True #required for the _id 
        json_encoders = {ObjectId: str}

class EnrollmentEdit(EnrollmentBase):
    pass
