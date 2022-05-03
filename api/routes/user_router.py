from bottle import route, get, post, put, delete, request
import api.controller.user_controller as user_ctrl
import api.controller.enrollment_controller as enrollment_ctrl
from .auth_router import requires_auth, get_jwt_credentials

@get('/users')
def get_all_users():
    return user_ctrl.get_all_users()

@get('/users/<id>')
def get_user_by_id(id):
    return user_ctrl.get_by_id(id)

@delete('/users/<id>')
def delete_user(id):
    return user_ctrl.delete_by_id(id)

@put('/users/<id>')
def edit_user(id):
    values = request.json
    return user_ctrl.edit_user(id, values)

@post('/users')
def create_user():
    values = request.json
    return user_ctrl.create_user(values)

@get('/users/enrollments')
@requires_auth
def get_user_enrollments():
    authenticated_user = get_jwt_credentials()
    print(authenticated_user['user'])
    user_id = authenticated_user['user']['id']
    print('in router', authenticated_user, user_id)
    return enrollment_ctrl.get_by_user(user_id)
