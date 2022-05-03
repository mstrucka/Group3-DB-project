from db.sql.sql import Session
from db.sql.lecture import Lecture
from db.sql.association_tables import course_lectures, course_progresses
import api.controller.course_controller as course_ctrl
import api.controller.enrollment_controller as enrollment_ctrl
from sqlalchemy import select, delete, update, insert

def get_all_lectures():
    with Session() as session:
        res = session.query(Lecture).all()
        lectures = [ el.to_dict() for el in res ]
    return dict(lectures=lectures)

def get_by_id(id):
    with Session() as session:
        stmt = select(Lecture).where(Lecture.id == id)
        res = session.execute(stmt).scalars().one()
        lecture = res.to_dict()
    return dict(lecture=lecture)

def delete_by_id(id):
    with Session.begin() as session:
        lecture = session.query(Lecture).filter(Lecture.id == id).one()
        session.delete(lecture)
        session.commit()
    return {}

def finish_lecture(user_id, lecture_id):
    with Session.begin() as session:
        # get lecture's course_id done 
        course_id = course_ctrl.get_by_lecture_id(lecture_id)
        # get enrollment based on course id & student id (and hope it isn't there multiple times)
        enrollment = enrollment_ctrl.get_by_user_id_and_course_id(course_id, user_id)

        values = {}
        values['finished_lecture_id'] = lecture_id
        values['enrollment_id'] = enrollment['id']
        session.execute(course_progresses.insert(), values)
        session.commit()

def edit_lecture(id, values):
    with Session.begin() as session:
        stmt = update(Lecture).where(Lecture.id == id).values(values)
        session.execute(stmt)

        stmt2 = select(Lecture).where(Lecture.id == id)
        res = session.execute(stmt2).scalars().one()
        updated_lecture = res.to_dict()

        session.commit()
    return dict(lecture=updated_lecture)

def create_lecture(values):
    # assign values for course_lectures assoc. table
    course_lectures_values = {}
    course_lectures_values['course_id'] = values['course_id']
    # remove course_id from values inserted into lecture
    del values['course_id']

    stmt = insert(Lecture).values(values)
    with Session.begin() as session:
        res = session.execute(stmt)
        row = session.get(Lecture, res.inserted_primary_key)
        lecture = row.to_dict()

        course_lectures_values['lecture_id']=lecture['id']
        session.execute(course_lectures.insert(), course_lectures_values)
        session.commit()
    return dict(lecture=lecture)
