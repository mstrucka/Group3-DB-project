from bottle import route, get, post, put, delete, request
import api.controller.payment_controller as payment_ctrl

@get('/payments')
def get_all_payments():
    return payment_ctrl.get_all_payments()

@get('/payments/<id>')
def get_payment_by_id(id):
    return payment_ctrl.get_by_id(id)

@delete('/payments/<id>')
def delete_payment(id):
    return payment_ctrl.delete_by_id(id)

@put('/payments/<id>')
def edit_payment(id):
    values = request.json
    return payment_ctrl.edit_payment(id, values)

@post('/payments')
def create_payment():
    values = request.json
    return payment_ctrl.create_payment(values)