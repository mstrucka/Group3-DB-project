import os, logging
import bottle
from bottle import route, get, run
import api.routes

@route('/')
def index():
    return { 'message': 'Welcome to dbfordevs mandatory assignment' }

def start_server():    
    if os.environ.get('APP_LOCATION') == 'heroku':
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
    else:
        run(host='localhost', port=8080, debug=True, reloader=True)
