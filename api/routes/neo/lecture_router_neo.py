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


@router.get('/{title}')
def get_lecture_by_title(title: str = Path(..., title='Lecture title')):
    return lecture_ctrl.get_by_title(title)


@router.get('/course/{name}')
def get_lecture_by_course_title(title: str = Path(..., name='Course title')):
    return lecture_ctrl.get_by_course_title(title)


@router.put('/{title}')
def edit_lecture(lecture: LectureUpdateSchema, title: str = Path(..., title='Lecture title')):
    return lecture_ctrl.edit_lecture(title, lecture)


@router.delete('/{title}')
def delete_lecture(title: str = Path(..., title='Lecture title')):
    return lecture_ctrl.delete_by_title(title)


@router.post('/')
def create_lecture(lecture: LectureCreateSchema):
    return lecture_ctrl.create_lecture(lecture)
