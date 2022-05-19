from fastapi import APIRouter, Path
import api.controller.neo.payment_controller as payment_ctrl
from db.neo4jdb.payment import PaymentCreateSchema

router = APIRouter(
    prefix='/payments',
    tags=['Payments']
)


@router.get('/')
def get_all_payments():
    return payment_ctrl.get_all_payments()


@router.get('/{id}')
def get_payment_by_id(id: str = Path(..., id='Payment id')):
    return payment_ctrl.get_by_id(id)


@router.delete('/{id}')
def delete_payment(id: str = Path(..., id='Payment id')):
    return payment_ctrl.delete_by_id(id)

@router.post('/')
def create_payment(payment: PaymentCreateSchema):
    return payment_ctrl.create_payment(payment)
