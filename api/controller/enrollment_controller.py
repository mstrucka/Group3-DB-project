from db.sql.sql import Session
from db.sql.enrollment import Enrollment
from sqlalchemy import select, delete, update, insert

def get_all_enrollments():
    with Session() as session:
        res = session.query(Enrollment).all()
        enrollments = [ el.to_dict() for el in res ]
    return dict(enrollments=enrollments)

def get_by_id(id):
    with Session() as session:
        stmt = select(Enrollment).where(Enrollment.id == id)
        res = session.execute(stmt).scalars().one()
        enrollment = res.to_dict()
    return dict(enrollment=enrollment)

def delete_by_id(id):
    with Session.begin() as session:
        delstmt = delete(Enrollment).where(Enrollment.id == id)
        x = session.execute(delstmt)
        session.commit()
    return { 'affected_rows': x.rowcount }

def edit_enrollment(id, values):
    with Session.begin() as session:
        stmt = update(Enrollment).where(Enrollment.id == id).values(values)
        session.execute(stmt)

        stmt2 = select(Enrollment).where(Enrollment.id == id)
        res = session.execute(stmt2).scalars().one()
        updated_enrollment = res.to_dict()

        session.commit()
    return dict(enrollment=updated_enrollment)

def create_enrollment(values):
    stmt = insert(Enrollment).values(values)
    with Session.begin() as session:
        res = session.execute(stmt)
        row = session.get(Enrollment, res.inserted_primary_key)
        enrollment = row.to_dict()
        session.commit()
    return dict(enrollment=enrollment)

def get_by_user(user_id):
    with Session() as session:
        res = session.query(Enrollment).filter(Enrollment.student_id == user_id).all()
        enrollments = [ el.to_dict() for el in res ]
    return dict(enrollments=enrollments)