from . models import MyMixin, Base
from . association_tables import lecture_resources
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

class Enrollment(Base, MyMixin, SerializerMixin):
    student_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    #course_id = Column(Integer, ForeignKey('course.id'), nullable=False, index=True)
    payment_id = Column(Integer, ForeignKey('payment.id'), nullable=False, index=True)
    finished = Column(Boolean)

    student = relationship('User')
    #course = relationship('Course')
    payment = relationship('Payment')


