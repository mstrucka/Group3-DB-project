from . models import MyMixin, Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

class Enrollment(Base, MyMixin, SerializerMixin):
    student_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    payment_id = Column(Integer, ForeignKey('payment.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    finished = Column(Boolean, nullable=False)


