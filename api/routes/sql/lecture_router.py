from api.controller.sql.auth_controller1 import get_current_user
import api.controller.sql.lecture_controller as lecture_ctrl
from fastapi import APIRouter, Depends, Path
from api.models.auth import User
from db.DbTypes import DbTypes
from db.sql.lecture import LectureCreate, LectureEdit

router = APIRouter(
    prefix='/lectures',
    tags=['lectures']
)

@router.get('/')
def get_all_lectures():
    return lecture_ctrl.get_all_lectures()

@router.get('/{id}')
def get_lecture_by_id(db: DbTypes, id: int = Path(..., title='Lecture ID')):
    return lecture_ctrl.get_by_id(id)

@router.delete('/{id}')
def delete_lecture(db: DbTypes, id: int = Path(..., title='Lecture ID')):
    return lecture_ctrl.delete_by_id(id)

@router.patch('/{id}')
def edit_lecture(db: DbTypes, lecture: LectureEdit, id: int = Path(..., title='Lecture ID')):
    values = lecture.dict(exclude_unset=True)
    return lecture_ctrl.edit_lecture(id, values)

@router.put('/finish/{id}')
def finish_lecture(db: DbTypes, id: int = Path(..., title='Lecture ID'), current_user: User = Depends(get_current_user)):
    return lecture_ctrl.finish_lecture(current_user.id, id)

@router.post('/')
def create_lecture(db: DbTypes, lecture: LectureCreate):
    values = lecture.dict(exclude_unset=True)
    return lecture_ctrl.create_lecture(values)