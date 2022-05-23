from fastapi import APIRouter, Depends, Path
from api.controller.mongo.auth_controller import get_current_user
import api.controller.mongo.user_controller as user_ctrl_mongo

router = APIRouter(
    prefix='/students',
    tags=['Students']
)

@router.get('/')
async def get_all():
    res = await user_ctrl_mongo.get_all_students()
    return res