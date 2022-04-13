from bottle import route, get, post, put, delete, request
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
    values = request.json
    return course_ctrl.edit_course(id, values)

@post('/courses')
def create_course():
    values = request.json
    return course_ctrl.create_course(values)

@get('/courses/search')
def search_courses():
    query = request.query.q
    limit = request.query.limit or 10
    return course_ctrl.search_courses(query, limit)