from bottle import route, get, post, put, delete, request
import api.controller.enrollment_controller as enrollment_ctrl

@get('/enrollments')
def get_all_enrollments():
    return enrollment_ctrl.get_all_enrollments()

@get('/enrollments/<id>')
def get_enrollment_by_id(id):
    return enrollment_ctrl.get_by_id(id)

@delete('/enrollments/<id>')
def delete_enrollment(id):
    return enrollment_ctrl.delete_by_id(id)

@put('/enrollments/<id>')
def edit_enrollment(id):
    values = request.json
    return enrollment_ctrl.edit_enrollment(id, values)

@post('/enrollments')
def create_enrollment():
    values = request.json
    return enrollment_ctrl.create_enrollment(values)