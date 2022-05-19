import string
from fastapi import APIRouter, Path
import api.controller.neo.course_controller as course_ctrl
from db.neo4jdb.course import CourseCreateSchema, CourseUpdateSchema

router = APIRouter(
    prefix='/courses',
    tags=['Courses']
)

# TODO: bidirectional relationships btw the things so that we can better search
@router.get('/')
def get_all_courses():
    return course_ctrl.get_all_courses()


@router.get('/{name}')
def get_course_by_name(name: string = Path(..., name='Course name')):
    return course_ctrl.get_by_name(name)

@router.get('/lectures/{name}')
def get_lectures_by_course_name(name: string = Path(..., name='Course name')):
    return course_ctrl.get_by_course_name(name)

@router.put('/{name}')
def edit_course(course: CourseUpdateSchema, name: string = Path(..., name='Course name')):
    return course_ctrl.edit_course(name, course)

@router.delete('/{name}')
def delete_course(name: string = Path(..., name='Course name')):
    return course_ctrl.delete_by_name(name)

@router.post('/')
def create_course(course: CourseCreateSchema):
    return course_ctrl.create_course(course)
