from fastapi import APIRouter, Path, Query, Body
import api.controller.sql.course_controller as course_ctrl
from db.sql.course import CourseCreate, CourseEdit
from db.DbTypes import DbTypes

router = APIRouter(
    prefix='/courses',
    tags=['courses'],
)

@router.get('/')
def get_all_courses(db: DbTypes):
    return course_ctrl.get_all_courses()

@router.get('/today')
def get_course_of_the_day(db: DbTypes):
    return course_ctrl.get_todays_course_of_the_day()

@router.get('/search')
def search_courses(
    db: DbTypes,
    q: str = Query(..., title='Search query'), 
    limit: int | None = Query(10, title='Limit results')):
    return course_ctrl.search_courses(q, limit)

@router.get('/{id}')
def get_course_by_id(db: DbTypes, id: int = Path(..., title='Course ID')):
    return course_ctrl.get_by_id(id)

@router.delete('/{id}')
def delete_course(db: DbTypes, id: int = Path(..., title='Course ID')):
    return course_ctrl.delete_by_id(id)

@router.patch('/{id}',)
async def edit_course(db: DbTypes, course: CourseEdit, id: int = Path(..., title='Course ID')):
    updated_values = course.dict(exclude_unset=True)
    return course_ctrl.edit_course(id, updated_values)

@router.post('/')
async def create_course(db: DbTypes, course: CourseCreate):
    values = course.dict(exclude_unset=True)
    return course_ctrl.create_course(values)