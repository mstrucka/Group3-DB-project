from fastapi import APIRouter, Path
import api.controller.neo.resource_controller as resource_ctrl
from db.neo4jdb.resource import ResourceCreate, ResourceUpdate

router = APIRouter(
    prefix='/resources',
    tags=['Resources']
)


@router.get('/')
def get_all_resources():
    return resource_ctrl.get_all_resources()


@router.get('/{name}')
def get_resource_by_name(name: str = Path(..., name='Resource name')):
    return resource_ctrl.get_by_name(name)


@router.get('/lecture/names/{name}')
def get_all_resources_for_lecture_names(name: str = Path(..., name='Lecture name')):
    return resource_ctrl.get_all_resources_for_lecture_names(name)


@router.get('/lecture/full/{name}')
def get_all_resources_for_lecture_full(name: str = Path(..., name='Lecture name')):
    return resource_ctrl.get_all_resources_for_lecture_full(name)


@router.delete('/{name}')
def delete_resource(name: str = Path(..., name='Resource name')):
    return resource_ctrl.delete_by_name(name)


@router.put('/{name}')
def edit_resource(resource: ResourceUpdate, name: str = Path(..., name='Resource name')):
    return resource_ctrl.edit_resource(name, resource)


@router.post('/')
def create_resource(resource: ResourceCreate):
    return resource_ctrl.create_resource(resource)
