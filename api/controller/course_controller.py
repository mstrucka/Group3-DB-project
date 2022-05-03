from db.sql.sql import Session
from db.sql.course import Course
from db.sql.association_tables import course_lectures
from sqlalchemy import select, delete, update, insert

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

def get_by_lecture_id(lecture_id):
    with Session() as session:
        res = session.execute(course_lectures.select().where(course_lectures.c.lecture_id == lecture_id))
        parsed_res = res.mappings().first()
    # TODO: works only if lecture_id isn't present more than once
    return parsed_res['course_id']

def delete_by_id(id):
    with Session.begin() as session:
        delstmt = delete(Course).where(Course.id == id)
        x = session.execute(delstmt)
        session.commit()
    return { 'affected_rows': x.rowcount }

def edit_course(id, values):
    with Session.begin() as session:
        stmt = update(Course).where(Course.id == id).values(values)
        session.execute(stmt)

        stmt2 = select(Course).where(Course.id == id)
        res = session.execute(stmt2).scalars().one()
        updated_course = res.to_dict()

        session.commit()
    return dict(course=updated_course)

def create_course(values):
    stmt = insert(Course).values(values)
    with Session.begin() as session:
        res = session.execute(stmt)
        row = session.get(Course, res.inserted_primary_key)
        course = row.to_dict()
        session.commit()
    return dict(course=course)

def search_courses(query, limit):
    with Session() as session:
        results = session.query(Course).filter(Course.title.ilike(f'%{query}%') | Course.description.ilike(f'%{query}%')).limit(limit).all()
        courses = [ el.to_dict() for el in results ]
    return dict(courses=courses)
