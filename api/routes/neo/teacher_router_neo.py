from fastapi import APIRouter, Path
import api.controller.neo.teacher_controller as teacher_ctrl
from db.neo4jdb.user import UserCreate, UserUpdate

router = APIRouter(
    prefix='/teachers',
    tags=['Teachers']
)


@router.get('/')
def get_all_teachers():
    res = teacher_ctrl.get_all_teachers()
    return res


@router.get('/{name}')
def get_teacher_by_name(name: str = Path(..., name='Teacher name')):
    return teacher_ctrl.get_by_name(name)


@router.get('/course/{name}')
def get_teacher_by_course_name(name: str = Path(..., name='Course name')):
    return teacher_ctrl.get_by_course_name(name)


@router.get('/courses/all/{name}')
def get_courses_taught_by_teacher(name: str = Path(..., name='Teacher name')):
    return teacher_ctrl.get_courses_taught_by_teacher(name)


@router.delete('/{name}')
def delete_teacher(name: str = Path(..., name='Teacher name')):
    return teacher_ctrl.delete_by_name(name)


@router.put('/{name}')
def edit_teacher(teacher: UserUpdate, name: str = Path(..., name='Teacher name')):
    return teacher_ctrl.edit_teacher(name, teacher)


@router.post('/')
def create_teacher(teacher: UserCreate):
    return teacher_ctrl.create_teacher(teacher)
