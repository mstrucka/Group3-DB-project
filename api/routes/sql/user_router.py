from fastapi import APIRouter, Depends, Path
from api.controller.sql.auth_controller1 import get_current_user
import api.controller.sql.user_controller as user_ctrl_sql
import api.controller.sql.enrollment_controller as enrollment_ctrl
from api.models.auth import User, UserEdit, UserInDB

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/')
def get_all_users():
    return user_ctrl_sql.get_all_users()

@router.get('/enrollments')
def get_user_enrollments(current_user: UserInDB = Depends(get_current_user)):
    return enrollment_ctrl.get_by_user(current_user.id)

@router.get('/{id}')
async def get_user_by_id(id: str = Path(..., title='User ID'), current_user: UserInDB = Depends(get_current_user)):
    return user_ctrl_sql.get_by_id(id)

@router.delete('/{id}')
def delete_user(id: int = Path(..., title='User ID')):
    return user_ctrl_sql.delete_by_id(id)

@router.put('/{id}')
def edit_user(user: UserEdit, id: int = Path(..., title='User ID')):
    values = user.dict(exclude_unset=True)
    return user_ctrl_sql.edit_user(id, values)

@router.post('/', deprecated=True)
def create_user(user: User):
    values = user.dict(exclude_unset=True)
    return user_ctrl_sql.create_user(values)