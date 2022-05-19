from fastapi import APIRouter, Depends, Path
from api.controller.mongo.auth_controller import get_current_user
import api.controller.mongo.payment_controller as payment_ctrl
from api.models.auth import User, UserInDB
from db.sql.payment import PaymentCreate, PaymentEdit

router = APIRouter(
    prefix='/payments',
    tags=['Payments']
)

@router.post('/', description='User can choose courses and pay for them, then he is enrolled')
async def create_payment(payment: PaymentCreate, current_user: UserInDB = Depends(get_current_user)):
    data = payment.dict(exclude_unset=True)
    res = await payment_ctrl.create_payment(current_user.mongo_id, data)
    return {'payment': res}