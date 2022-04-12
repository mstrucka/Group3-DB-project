from bottle import route, get, post, put, delete, request
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

@post('/lectures')
def create_lecture():
    values = request.json
    return lecture_ctrl.create_lecture(values)