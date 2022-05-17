from fastapi import APIRouter, Path, Query, Body
import api.controller.sql.resource_controller as resource_ctrl
from db.sql.resource import ResourceCreate, ResourceEdit

router = APIRouter(
    prefix='/resources',
    tags=['Resources']
)

@router.get('/')
def get_all_resources():
    return resource_ctrl.get_all_resources()

@router.get('/{id}')
def get_resource_by_id(id: int = Path(..., title='Resource ID')):
    return resource_ctrl.get_by_id(id)

@router.delete('/{id}')
def delete_resource(id: int = Path(..., title='Resource ID')):
    return resource_ctrl.delete_by_id(id)

@router.put('/{id}')
def edit_resource(resource: ResourceEdit, id: int = Path(..., title='Resource ID')):
    values = resource.dict(exclude_unset=True)
    return resource_ctrl.edit_resource(id, values)

@router.post('/')
def create_resource(resource: ResourceCreate):
    values = resource.dict()
    return resource_ctrl.create_resource(values)