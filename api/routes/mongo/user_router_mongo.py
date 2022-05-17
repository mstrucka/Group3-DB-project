from fastapi import APIRouter, Depends, Path
from api.controller.mongo.auth_controller import get_current_user
import api.controller.mongo.user_controller as user_ctrl_mongo
import api.controller.mongo.enrollment_controller as enrollment_ctrl
from api.models.auth import User, UserEdit, UserInDB
from db.mongodb.user import UserSchema

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/')
async def get_all_users():
    res = await user_ctrl_mongo.get_all_users()
    return res

@router.get('/enrollments')
def get_user_enrollments(current_user: UserInDB = Depends(get_current_user)):
    return enrollment_ctrl.get_by_user(current_user.id)

@router.get('/{id}')
async def get_user_by_id(id: str = Path(..., title='User ID')):
    user = await user_ctrl_mongo.get_user_by_id(id)
    x = UserSchema(**user)
    return x

@router.delete('/{id}')
async def delete_user(id: int | str = Path(..., title='User ID')):
    res = await user_ctrl_mongo.delete_by_id(id)
    return res

@router.put('/{id}')
async def edit_user(user: UserEdit, id: int | str = Path(..., title='User ID')):
    values = user.dict(exclude_unset=True)
    res = await user_ctrl_mongo.edit_user(id, values)
    return res

@router.post('/', deprecated=True)
async def create_user(user: User):
    values = user.dict(exclude_unset=True)
    new_user = await user_ctrl_mongo.create_user(values)
    return UserInDB(**new_user)