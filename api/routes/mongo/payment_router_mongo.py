from fastapi import APIRouter, Depends, Path
from api.controller.mongo.auth_controller import get_current_user
import api.controller.mongo.payment_controller as payment_ctrl
from api.models.auth import User, UserInDB
from db.sql.payment import PaymentCreate, PaymentEdit

router = APIRouter(
    prefix='/payments',
    tags=['Payments']
)

@router.get('/')
def get_all_payments():
    return payment_ctrl.get_all_payments()

@router.get('/{id}')
def get_payment_by_id(id: int = Path(..., title='Payment ID')):
    return payment_ctrl.get_by_id(id)

@router.delete('/{id}')
def delete_payment(id: int = Path(..., title='Payment ID')):
    return payment_ctrl.delete_by_id(id)

@router.put('/{id}')
def edit_payment(payment: PaymentEdit, id: int = Path(..., title='Payment ID')):
    values = payment.dict(exclude_unset=True)
    return payment_ctrl.edit_payment(id, values)

@router.post('/')
async def create_payment(payment: PaymentCreate, current_user: UserInDB = Depends(get_current_user)):
    data = payment.dict(exclude_unset=True)
    res = await payment_ctrl.create_payment(current_user.mongo_id, data)
    return res