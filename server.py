import os
from bottle import route, run
from db.sql import Session

@route('/')
def index():
    with Session.begin() as session:
        result = session.execute('SELECT * FROM USERS').all()
    return { 'result': True }

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)