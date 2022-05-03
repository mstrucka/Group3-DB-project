from bottle import route, get, post, put, delete, request
from api.controller.auth_controller import get_user_id_from_jwt, requires_auth
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
@requires_auth
def create_payment():
    user_id = get_user_id_from_jwt()
    values = request.json
    return payment_ctrl.create_payment(user_id, values)