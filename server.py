import os, json
from bottle import route, run
from db.sql.sql import Session
from db.sql.user import User

@route('/')
def index():
    #u = User(firstName='John', lastName='Hitler', email='j@h.reich', password='sfjsd98sdfj', dob='1995-12-12', isStudent=True)
    with Session() as session:
        u = session.query(User).filter_by(firstName='John').one()
    return { 'result': u.to_dict() }
if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)