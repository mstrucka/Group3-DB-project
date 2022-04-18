import os
from bottle import route, run

import api.routes.course_router
import api.routes.lecture_router
import api.routes.enrollment_router
import api.routes.payment_router
import api.routes.resource_router
import api.routes.user_router
import api.routes.auth_router

@route('/')
def index():
    return { 'message': 'Welcome to dbfordevs mandatory assignment' }

def start_server():    
    if os.environ.get('APP_LOCATION') == 'heroku':
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        run(host='localhost', port=8080, debug=True, reloader=True)
