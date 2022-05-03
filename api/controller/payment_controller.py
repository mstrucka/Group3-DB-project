from datetime import datetime
from db.sql.sql import Session
from db.sql.payment import Payment
from sqlalchemy import false, select, delete, update, insert
import api.controller.course_controller as course_ctrl

def get_all_payments():
    with Session() as session:
        res = session.query(Payment).all()
        payments = [ el.to_dict() for el in res ]
    return dict(payments=payments)

def get_by_id(id):
    with Session() as session:
        stmt = select(Payment).where(Payment.id == id)
        res = session.execute(stmt).scalars().one()
        payment = res.to_dict()
    return dict(payment=payment)

def delete_by_id(id):
    with Session.begin() as session:
        payment = session.query(Payment).filter(Payment.id == id).one()
        session.delete(payment)
        session.commit()
    return {}

def edit_payment(id, values):
    with Session.begin() as session:
        stmt = update(Payment).where(Payment.id == id).values(values)
        session.execute(stmt)

        stmt2 = select(Payment).where(Payment.id == id)
        res = session.execute(stmt2).scalars().one()
        updated_payment = res.to_dict()

        session.commit()
    return dict(payment=updated_payment)

def create_payment(user_id, values):
    course_ids = values['course_ids']
    total_price = 0.0
    with Session.begin() as session:
        for course_id in course_ids:
            course = course_ctrl.get_by_id(course_id)
            total_price += float(course['course']['price'])

        values['total'] = total_price
        del values['course_ids']

        stmt = insert(Payment).values(values)
        res = session.execute(stmt)
        row = session.get(Payment, res.inserted_primary_key)
        payment = row.to_dict()
        session.commit()
    return dict(payment=payment)
