from fastapi import APIRouter, Path, Query, Body
import api.controller.mongo.course_controller as course_ctrl
from db.sql.course import CourseCreate, CourseEdit
from db.DbTypes import DbTypes
from db.mongodb.course import CourseSchema, CourseEditSchema

router = APIRouter(
    prefix='/courses',
    tags=['courses'],
)

@router.get('/')
async def get_all_courses():
    res = await course_ctrl.get_all_courses()
    return res

@router.get('/today')
async def get_course_of_the_day():
    res = await course_ctrl.get_course_of_the_day()
    return res

@router.get('/search')
async def search_courses(
    q: str = Query(..., title='Search query'), 
    limit: int | None = Query(10, title='Limit results')):
    courses = await course_ctrl.search_courses(q, limit)
    return courses

@router.get('/{id}')
async def get_course_by_id(id: str = Path(..., title='Course ID')):
    course = await course_ctrl.get_course_by_id(id)
    return CourseSchema(**course)

@router.delete('/{id}')
async def delete_course(id: int = Path(..., title='Course ID')):
    res = await course_ctrl.delete_course_by_id(id)
    return res

@router.patch('/{id}')
async def edit_course(course: CourseEditSchema, id: str = Path(..., title='Course ID')):
    updated_values = course.dict(exclude_unset=True)
    res = await course_ctrl.edit_course(id, updated_values)
    if type(res) is bool:
        return res
    return CourseSchema(**res)

@router.post('/')
async def create_course(course: CourseSchema):
    data = course.dict(exclude_unset=True)
    res = await course_ctrl.create_course(data)
    return CourseSchema(**res)