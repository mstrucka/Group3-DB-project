from db.sql.sql import Session
from db.sql.course import Course
from sqlalchemy import select, delete

def get_all_courses():
    with Session() as session:
        res = session.query(Course).all()
        courses = [ el.to_dict() for el in res ]
    return dict(courses=courses)

def get_by_id(id):
    with Session() as session:
        stmt = select(Course).where(Course.id == id)
        res = session.execute(stmt).scalars().one()
        course = res.to_dict()
    return dict(course=course)

def delete_by_id(id):
    with Session.begin() as session:
        course = session.query(Course).filter(Course.id == id).one()
        session.delete(course)
        session.commit()
    return {}
