from . models import MyMixin, Base
from . association_tables import course_lectures
from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
class Course(MyMixin, SerializerMixin, Base):
    title = Column(String(45), nullable=False)
    description = Column(String(500), nullable=False)
    level = Column(Integer)
    price = Column(Numeric(7, 2), nullable=False)
    platform_sale = Column(Boolean)
    category = Column(String(45))
    lecturer_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))

    course_of_the_day = relationship('CourseOfTheDay')
    lectures = relationship('Lecture', secondary=course_lectures)
    course = relationship('Enrollment', cascade='all, delete')

    Index('course_title_price_idx', title.desc(), price.desc())
    Index('course_category_idx', category.asc())
    Index('lecturer_id_idx', lecturer_id.asc())

    def __repr__(self) -> str:
        return f'''<Course(id={self.id}, title={self.title})>'''