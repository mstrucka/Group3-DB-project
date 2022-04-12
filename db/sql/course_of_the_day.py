from . models import Base
from sqlalchemy import Column, Date, Integer, ForeignKey

class CourseOfTheDay(Base):
    __tablename__ = 'courses_of_the_day'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__= {'always_refresh': True}

    date = Column(Date, nullable=False, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self) -> str:
        return f'''<CourseOfTheDay (course_id={self.course_id}, date={self.date})>'''