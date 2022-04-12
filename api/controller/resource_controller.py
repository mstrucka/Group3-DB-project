from db.sql.sql import Session
from db.sql.resource import Resource
from sqlalchemy import select, delete, update, insert

def get_all_resources():
    with Session() as session:
        res = session.query(Resource).all()
        resources = [ el.to_dict() for el in res ]
    return dict(resources=resources)

def get_by_id(id):
    with Session() as session:
        stmt = select(Resource).where(Resource.id == id)
        res = session.execute(stmt).scalars().one()
        resource = res.to_dict()
    return dict(resource=resource)

def delete_by_id(id):
    with Session.begin() as session:
        resource = session.query(Resource).filter(Resource.id == id).one()
        session.delete(resource)
        session.commit()
    return {}

def edit_resource(id, values):
    with Session.begin() as session:
        stmt = update(Resource).where(Resource.id == id).values(values)
        session.execute(stmt)

        stmt2 = select(Resource).where(Resource.id == id)
        res = session.execute(stmt2).scalars().one()
        updated_resource = res.to_dict()

        session.commit()
    return dict(resource=updated_resource)

def create_resource(values):
    stmt = insert(Resource).values(values)
    with Session.begin() as session:
        res = session.execute(stmt)
        row = session.get(Resource, res.inserted_primary_key)
        resource = row.to_dict()
        session.commit()
    return dict(resource=resource)
