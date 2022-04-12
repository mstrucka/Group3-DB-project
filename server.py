
from db.sql.enrollment import Enrollment

import os
from bottle import route, run, get
from db.sql.sql import Session
from db.sql.user import User
from sqlalchemy import select

import api.routes.course_router
import api.routes.lecture_router
import api.routes.enrollment_router
import api.routes.payment_router
import api.routes.resource_router
import api.routes.user_router

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

def start_server():    
    if os.environ.get('APP_LOCATION') == 'heroku':
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        run(host='localhost', port=8080, debug=True, reloader=True)
