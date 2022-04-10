from bottle import route, get, post, put, delete
import api.controller.course_controller as course_ctrl

@get('/courses')
def get_all_courses():
    return course_ctrl.get_all_courses()

@get('/courses/<id>')
def get_course_by_id(id):
    return course_ctrl.get_by_id(id)

@delete('/courses/<id>')
def delete_course(id):
    return course_ctrl.delete_by_id(id)

@put('/courses/<id>')
def edit_course(id):
    pass

@post('/courses')
def create_course():
    pass