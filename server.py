from dotenv import load_dotenv
load_dotenv()
import os, json
from bottle import route, run, get
from db.sql.sql import Session
from db.sql.user import User
from db.sql.course import Course
from sqlalchemy.orm import lazyload
from sqlalchemy import select

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

@route('/test')
def get_course_and_lecturer():
    with Session() as session:
        # v1.x syntax
        """ res = session.query(Course).options(lazyload(Course.lecturer)).first()
        course = res.to_dict() """

        # v2.0 syntax
        stmt = select(Course).join(User)
        res = session.execute(stmt).scalars().first()
        course = res.to_dict()

    return { 'result': course }

@get('/users')
def get_users():
    # idea for how to deal with multiple rows
    # v2.0 syntax used
    with Session() as session:
        stmt = select(User)
        res = session.execute(stmt).scalars().all()
        users = [ el.to_dict() for el in res ]
    return { 'users': users }

@get('/courses')
def get_courses():
    # same as above, but using v1.x syntax
    with Session() as session:
        res = session.query(Course).options(lazyload(Course.lecturer)).all()
        courses = [ el.to_dict() for el in res ]
    return { 'courses': courses }

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True, reloader=True)