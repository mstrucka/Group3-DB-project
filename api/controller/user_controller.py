from db.sql.sql import Session
from db.sql.user import User
from sqlalchemy import select, delete, update, insert

def get_all_users():
    with Session() as session:
        res = session.query(User).all()
        users = [ el.to_dict() for el in res ]
    return dict(users=users)

def get_by_id(id):
    with Session() as session:
        stmt = select(User).where(User.id == id)
        res = session.execute(stmt).scalars().one()
        user = res.to_dict()
    return dict(user=user)

def delete_by_id(id):
    with Session.begin() as session:
        user = session.query(User).filter(User.id == id).one()
        session.delete(user)
        session.commit()
    return {}

def edit_user(id, values):
    with Session.begin() as session:
        stmt = update(User).where(User.id == id).values(values)
        session.execute(stmt)

        stmt2 = select(User).where(User.id == id)
        res = session.execute(stmt2).scalars().one()
        updated_user = res.to_dict()

        session.commit()
    return dict(user=updated_user)

def create_user(values):
    stmt = insert(User).values(values)
    with Session.begin() as session:
        res = session.execute(stmt)
        row = session.get(User, res.inserted_primary_key)
        user = row.to_dict()
        session.commit()
    return dict(user=user)
