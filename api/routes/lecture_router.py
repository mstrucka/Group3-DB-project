from bottle import route, get, post, put, delete, request
from api.controller.auth_controller import get_user_id_from_jwt, requires_auth
import api.controller.lecture_controller as lecture_ctrl

@get('/lectures')
def get_all_lectures():
    return lecture_ctrl.get_all_lectures()

@get('/lectures/<id>')
def get_lecture_by_id(id):
    return lecture_ctrl.get_by_id(id)

@delete('/lectures/<id>')
def delete_lecture(id):
    return lecture_ctrl.delete_by_id(id)

@put('/lectures/<id>')
def edit_lecture(id):
    values = request.json
    return lecture_ctrl.edit_lecture(id, values)

@put('/courses/lectures/<id>')
@requires_auth
def finish_lecture(id):
    user_id = get_user_id_from_jwt()
    return lecture_ctrl.finish_lecture(user_id, id)

@post('/lectures')
def create_lecture():
    values = request.json
    return lecture_ctrl.create_lecture(values)