from fastapi import APIRouter, Path, Query, Request, Body
import api.controller.enrollment_controller as enrollment_ctrl
from db.DbTypes import DbTypes
from db.sql.enrollment import EnrollmentEdit

router = APIRouter(
    prefix='/enrollments',
    tags=['enrollments']
)

@router.get('/')
def get_all_enrollments(db: DbTypes):
    return enrollment_ctrl.get_all_enrollments()

@router.get('/{id}')
def get_enrollment_by_id(db: DbTypes, id: int = Path(..., title='Enrollment ID')):
    return enrollment_ctrl.get_by_id(id)

@router.delete('/{id}')
def delete_enrollment(db: DbTypes, id: int = Path(..., title='Enrollment ID')):
    return enrollment_ctrl.delete_by_id(id)

@router.patch('/{id}')
def edit_enrollment(db: DbTypes, enrollment: EnrollmentEdit, id: int = Path(..., title='Enrollment ID')):
    values = enrollment.dict(exclude_unset=True)
    return enrollment_ctrl.edit_enrollment(id, values)
