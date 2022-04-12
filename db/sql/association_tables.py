from sqlalchemy import ForeignKey, Column, Table
from . models import Base

course_lectures = Table('course_lectures', Base.metadata,
    Column('course_id', ForeignKey('course.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, index=True),
    Column('lecture_id', ForeignKey('lecture.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, index=True),
)

course_progresses = Table('course_progresses', Base.metadata,
    Column('enrollment_id', ForeignKey('enrollment.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, index=True),
    Column('finished_lecture_id', ForeignKey('lecture.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, index=True),
)

lecture_resources = Table('lecture_resources', Base.metadata,
    Column('lecture_id', ForeignKey('lecture.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, index=True),
    Column('resource_id', ForeignKey('resource.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, index=True),
)

