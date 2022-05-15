from fastapi import APIRouter, Depends, Path, Query, Body
from api.controller.auth_controller1 import get_current_user
import api.controller.user_controller as user_ctrl
import api.controller.enrollment_controller as enrollment_ctrl
from api.models.auth import User, UserEdit, UserInDB

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/')
def get_all_users():
    return user_ctrl.get_all_users()

@router.get('/enrollments')
def get_user_enrollments(current_user: UserInDB = Depends(get_current_user)):
    print(current_user.id, type(current_user.id))
    return enrollment_ctrl.get_by_user(current_user.id)

@router.get('/{id}')
def get_user_by_id(id: int = Path(..., title='User ID')):
    return user_ctrl.get_by_id(id)

@router.delete('/{id}')
def delete_user(id: int = Path(..., title='User ID')):
    return user_ctrl.delete_by_id(id)

@router.put('/{id}')
def edit_user(user: UserEdit, id: int = Path(..., title='User ID')):
    values = user.dict(exclude_unset=True)
    return user_ctrl.edit_user(id, values)

@router.post('/', deprecated=True)
def create_user(user: User):
    values = user.dict(exclude_unset=True)
    return user_ctrl.create_user(values)