import api.controller.auth_controller as auth_ctrl
import logging
from api.controller.auth_controller import requires_auth, get_jwt_credentials
from bottle import get, post, request, abort

@post('/login')
def login_authenticate():
    return auth_ctrl.authenticate()

@post('/register')
def register():
    values = request.json
    return auth_ctrl.register(values)

@get('/protected/resource')
@requires_auth
def get_protected_resource():
    # get user details from JWT
    authenticated_user = get_jwt_credentials()
    
    # get protected resource
    try:
        return { 'message': 'success!', 'user': authenticated_user }
    except Exception as e:
        logging.exception("Resource not found", e)
        abort(404, 'No resource for username %s was found.' % authenticated_user['user'])