from fastapi import APIRouter, Path
import api.controller.neo.lecture_controller as lecture_ctrl
from db.neo4jdb.lecture import LectureCreate, LectureUpdate

router = APIRouter(
    prefix='/lectures',
    tags=['Lectures']
)


@router.get('/')
def get_all_lectures():
    return lecture_ctrl.get_all_lectures()


@router.get('/{name}')
def get_lecture_by_name(name: str = Path(..., name='Lecture name')):
    return lecture_ctrl.get_by_name(name)


@router.put('/{name}')
def edit_lecture(lecture: LectureUpdate, name: str = Path(..., name='Lecture name')):
    return lecture_ctrl.edit_lecture(name, lecture)


@router.delete('/{name}')
def delete_lecture(name: str = Path(..., name='Lecture name')):
    return lecture_ctrl.delete_by_name(name)


@router.post('/')
def create_lecture(lecture: LectureCreate):
    return lecture_ctrl.create_lecture(lecture)
