from bottle import route, get, post, put, delete, request
import api.controller.resource_controller as resource_ctrl

@get('/resources')
def get_all_resources():
    return resource_ctrl.get_all_resources()

@get('/resources/<id>')
def get_resource_by_id(id):
    return resource_ctrl.get_by_id(id)

@delete('/resources/<id>')
def delete_resource(id):
    return resource_ctrl.delete_by_id(id)

@put('/resources/<id>')
def edit_resource(id):
    values = request.json
    return resource_ctrl.edit_resource(id, values)

@post('/resources')
def create_resource():
    values = request.json
    return resource_ctrl.create_resource(values)