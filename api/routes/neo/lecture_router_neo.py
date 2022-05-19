from fastapi import APIRouter, Path
import api.controller.neo.lecture_controller as lecture_ctrl
from db.neo4jdb.lecture import LectureCreateSchema, LectureUpdateSchema

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


@router.get('/course/{name}')
def get_lecture_by_course_name(name: str = Path(..., name='Course name')):
    return lecture_ctrl.get_by_course_name(name)


@router.put('/{name}')
def edit_lecture(lecture: LectureUpdateSchema, name: str = Path(..., name='Lecture name')):
    return lecture_ctrl.edit_lecture(name, lecture)


@router.delete('/{name}')
def delete_lecture(name: str = Path(..., name='Lecture name')):
    return lecture_ctrl.delete_by_name(name)


@router.post('/')
def create_lecture(lecture: LectureCreateSchema):
    return lecture_ctrl.create_lecture(lecture)
