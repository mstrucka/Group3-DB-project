from db.sql.sql import Session
from db.sql.lecture import Lecture
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
    stmt = insert(Lecture).values(values)
    with Session.begin() as session:
        res = session.execute(stmt)
        row = session.get(Lecture, res.inserted_primary_key)
        lecture = row.to_dict()
        session.commit()
    return dict(lecture=lecture)
