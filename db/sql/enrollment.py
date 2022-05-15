from . models import MyMixin, Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from pydantic import BaseModel

class Enrollment(Base, MyMixin, SerializerMixin):
    student_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    payment_id = Column(Integer, ForeignKey('payment.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    finished = Column(Boolean, nullable=False, default=False)

    course = relationship('Course', cascade='all, delete')
    payment = relationship('Payment')
    student = relationship('User')

class EnrollmentBase(BaseModel):
    student_id: int | None
    course_id: int | None
    payment_id: int | None
    finished: bool | None

class EnrollmentEdit(EnrollmentBase):
    pass
