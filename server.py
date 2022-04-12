
from db.sql.enrollment import Enrollment

import os
from bottle import route, run, get
from db.sql.sql import Session
from db.sql.user import User
from sqlalchemy import select

import api.routes.course_router
import api.routes.lecture_router

@route('/')
def index():
    with Session() as session:
        # below is how to query using v2.0 syntax
        statement = select(User).filter_by(firstname='Darth')
        result = session.execute(statement).scalars().first()
        user = result.to_dict()

        # this is with v1.x syntax
        #u = session.query(User).filter(User.email.like('%reich%')).one()
    return { 'result': user }

@get('/users')
def get_users():
    # idea for how to deal with multiple rows
    # v2.0 syntax used
    with Session() as session:
        stmt = select(User)
        res = session.execute(stmt).scalars().all()
        users = [ el.to_dict() for el in res ]
    return { 'users': users }

@get('/enrollments')
def get_enrollments():
    with Session() as session:
        res = session.query(Enrollment).all()
        enrollments = [ el.to_dict() for el in res ]
    return { 'enrollments': enrollments }

def start_server():    
    if os.environ.get('APP_LOCATION') == 'heroku':
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        run(host='localhost', port=8080, debug=True, reloader=True)
