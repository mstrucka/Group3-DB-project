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


@router.get('/{title}')
def get_course_by_title(title: str = Path(..., title='Course title')):
    return course_ctrl.get_by_title(title)


@router.get('/lectures/{title}')
def get_lectures_by_course_title(title: str = Path(..., title='Course title')):
    return course_ctrl.get_by_course_title(title)


@router.put('/{title}')
def edit_course(course: CourseUpdate, title: str = Path(..., name='Course title')):
    return course_ctrl.edit_course(title, course)


@router.delete('/{title}')
def delete_course(title: str = Path(..., title='Course title')):
    return course_ctrl.delete_by_title(title)


@router.post('/')
def create_course(course: CourseCreate):
    return course_ctrl.create_course(course)
