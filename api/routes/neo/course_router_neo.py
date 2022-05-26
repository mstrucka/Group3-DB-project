from fastapi import APIRouter, Path
import api.controller.neo.course_controller as course_ctrl
from db.neo4jdb.course import CourseCreate, CourseUpdate

router = APIRouter(
    prefix='/courses',
    tags=['Courses']
)


@router.get('/')
def get_all_courses():
    return course_ctrl.get_all_courses()


@router.get('/{name}')
def get_course_by_name(name: str = Path(..., name='Course name')):
    return course_ctrl.get_by_name(name)


@router.get('/lectures/{name}')
def get_lectures_by_course_name(name: str = Path(..., name='Course name')):
    return course_ctrl.get_by_course_name(name)


@router.put('/{name}')
def edit_course(course: CourseUpdate, name: str = Path(..., name='Course name')):
    return course_ctrl.edit_course(name, course)


@router.delete('/{name}')
def delete_course(name: str = Path(..., name='Course name')):
    return course_ctrl.delete_by_name(name)


@router.post('/')
def create_course(course: CourseCreate):
    return course_ctrl.create_course(course)
