from fastapi import APIRouter, Path
import api.controller.neo.student_controller as student_ctrl
from db.neo4jdb.user import UserCreate, UserUpdate

router = APIRouter(
    prefix='/students',
    tags=['Students']
)


@router.get('/')
def get_all_students():
    return student_ctrl.get_all_students()


@router.get('/{name}')
def get_student_by_name(name: str = Path(..., name='Student name')):
    return student_ctrl.get_by_name(name)


@router.delete('/{name}')
def delete_student(name: str = Path(..., name='Student name')):
    return student_ctrl.delete_by_name(name)


@router.put('/{name}')
def edit_student(student: UserUpdate, name: str = Path(..., name='Student name')):
    return student_ctrl.edit_student(name, student)


@router.post('/')
def create_student(student: UserCreate):
    return student_ctrl.create_student(student)
